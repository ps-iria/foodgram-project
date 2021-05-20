from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas

from recipes import services
from recipes.forms import CreateRecipeForm
from recipes.models import Recipe

User = get_user_model()


def recipe_list(request):
    queryset = Recipe.objects.all()
    content = services.get_content(request, queryset)
    return render(
        request,
        "index.html",
        content
    )


@login_required()
def recipe_new(request):
    form = CreateRecipeForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            'new_recipe.html',
            {
                'form': form,
            }
        )
    ingredients = services.get_ingredients(request)
    context = services.validate_ingredients(form, ingredients)
    if context:
        return render(request, 'new_recipe.html', context)
    services.save_recipe(request, form, ingredients)
    return redirect("index")


def recipe(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    return render(
        request,
        "recipe.html",
        {
            "recipe": recipe,
        }
    )


@login_required
def recipe_edit(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if recipe.author != request.user:
        return redirect("index")
    form = CreateRecipeForm(request.POST or None,
                            files=request.FILES or None,
                            instance=recipe)
    if form.is_valid():
        ingredients = services.get_ingredients(request)
        context = services.validate_ingredients(form, ingredients)
        if context:
            return render(request, 'new_recipe.html',
                          context)
        services.save_recipe(request, form, ingredients)
        return redirect('index')
    return render(
        request,
        'new_recipe.html',
        {
            'form': form,
            'recipe': recipe
        }
    )


@login_required
def recipe_delete(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if recipe.author == request.user:
        recipe.delete()
        return redirect("index")
    return redirect("recipe", recipe_slug=recipe.slug)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    queryset = author.recipes.all()
    content = services.get_content(request, queryset)
    content["author"] = author
    return render(
        request,
        "profile.html",
        content
    )


def purchase(request):
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(
            purchase__user=request.user
        )
    else:
        recipes_ids = request.session.get('recipe_ids')
        if recipes_ids is not None:
            recipes = Recipe.objects.filter(pk__in=recipes_ids)
        else:
            recipes = []
    return render(
        request,
        'shop_cart.html',
        {
            'recipes': recipes,
        }
    )


def download_purchase(request):
    content = ''
    if request.user.is_authenticated:
        recipes = Recipe.objects.filter(purchase__user=request.user)
    else:

        recipes_ids = request.session.get('recipe_ids')
        if recipes_ids is not None:
            recipes = Recipe.objects.filter(pk__in=recipes_ids)
    ingredients = recipes.order_by('ingredient__title').values(
        'ingredient__title',
        'ingredient__dimension').annotate(
        total_count=Sum('counts__count'))
    for ingredient in ingredients:
        ingredient_str = (f'{ingredient["ingredient__title"]} - '
                          f'{ingredient["total_count"]} '
                          f'{ingredient["ingredient__dimension"]}')
        content += f'{ingredient_str}' + '\n'
    filename = 'recipe_ingredients.pdf'
    response = HttpResponse(content=content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    buffer = BytesIO()
    MyFontObject = ttfonts.TTFont('Arial', 'arial.ttf')
    pdfmetrics.registerFont(MyFontObject)
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Arial", 9)
    p.drawString(260, 810, 'Список покупок:')
    x1 = 20
    y1 = 780
    for key in ingredients:
        p.drawString(
            x1,
            y1 - 12,
            (f'{key["ingredient__title"]} - '
             f'{key["total_count"]} '
             f'{key["ingredient__dimension"]}')
        )
        y1 -= 20
        p.setTitle("Список покупок")
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


@login_required()
def follow_list(request):
    queryset = request.user.follower.all()
    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    page = services.pagination(paginator, page_number)
    return render(
        request,
        "follow.html",
        {
            "page": page,
            "paginator": paginator,
        }
    )


@login_required()
def favorite_list(request):
    queryset = Recipe.objects.filter(favorite__user=request.user)
    content = services.get_content(request, queryset)
    return render(
        request,
        "favorite.html",
        content
    )
