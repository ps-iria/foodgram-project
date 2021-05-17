from io import BytesIO

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, \
    InvalidPage
from django.db import transaction, IntegrityError
from django.db.models import Sum
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas

from recipes import services
from recipes.forms import CreateRecipeForm
from recipes.models import Recipe, RecipeIngredient, Tag

User = get_user_model()
TAGS = ["Завтрак", "Обед", "Ужин"]


def get_active_tags(request):
    """Получить список активных тегов для фильтрации рецептов"""
    tags = set()
    if 'tags' in request.GET:
        tags = set(request.GET.getlist('tags'))
        tags.intersection_update(set(TAGS))
    return tags


# @cache_page(20)
def RecipeList(request):
    queryset = Recipe.objects.all()
    active_tags = get_active_tags(request)
    if active_tags:
        queryset = services.filter_by_tags(queryset, active_tags)

    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    page = pagination(paginator, page_number)
    tags = Tag.objects.all()
    return render(
        request,
        "index.html",
        {
            "page": page,
            "tags": tags,
            "paginator": paginator,
            'active_tags': active_tags,
        }
    )


def pagination(paginator, page_number):
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    except InvalidPage:
        page = paginator.page(1)
    return page


@login_required()
def RecipeNew(request):
    form = CreateRecipeForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            'new_recipe.html',
            {
                'form': form,
            }
        )

    # save_recipe(request, form)
    ingredients = services.get_ingredients(request)
    context = services.validate_ingredients(form, ingredients)
    if context:
        return render(request, 'new_recipe.html', context)
    # recipe = form.save(commit=False)
    # recipe.author = request.user
    # recipe.slug = slugify(form.cleaned_data['title'])
    # recipe.save()
    services.save_recipe(request, form, ingredients)
    return redirect("index")


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(
        request,
        "recipe.html",
        {
            "recipe": recipe,
        }
    )


def recipe_slug(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    return render(
        request,
        "recipe.html",
        {
            "recipe": recipe,
        }
    )


def edit_recipe(request, form, instance):
    try:
        with transaction.atomic():
            RecipeIngredient.objects.filter(recipe=instance).delete()
            return services.save_recipe(request, form)
    except IntegrityError:
        raise HttpResponseBadRequest


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author != request.user:
        return redirect("index")
    form = CreateRecipeForm(request.POST or None,
                            files=request.FILES or None,
                            instance=recipe)
    if form.is_valid():
        # edit_recipe(request, form, instance=recipe)

        #     return redirect("recipe", recipe_id=recipe.id)
        # return render(request, "new_recipe.html", {
        #     "form": form,
        #     "recipe": recipe,
        #     }
        ingredients = services.get_ingredients(request)
        context = services.validate_ingredients(form, ingredients)
        if context:
            return render(request, 'new_recipe.html', context)

        # form.save_recipe(request)
        services.save_recipe(request, form, ingredients)
        return redirect('index')
    return render(request, 'new_recipe.html', {'form': form,
                                               'recipe': recipe}
                  )


@login_required
def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if recipe.author == request.user:
        recipe.delete()
        return redirect("index")
    return redirect("recipe", recipe_id=recipe.id)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    queryset = author.recipes.all()
    active_tags = get_active_tags(request)
    if active_tags:
        queryset = services.filter_by_tags(queryset, active_tags)

    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    page = pagination(paginator, page_number)
    tags = Tag.objects.all()
    return render(
        request,
        "profile.html",
        {
            "page": page,
            "tags": tags,
            "author": author,
            "paginator": paginator,
            'active_tags': active_tags,
        }
    )
    # context = services.get_context(request, recipes_list)
    # context['title'] = author.get_full_name()
    # context['author'] = author
    # return render(request, 'index.html', context)


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
    # print(recipes)
    return render(
        request,
        'shop_cart.html',
        {
            'recipes': recipes,
        }
    )


def delete_purchase(request, recipe_id):
    # Purchase.objects.get(id=recipe_id).delete()
    # recipes = Purchase.objects.filter(user=request.user)
    # return render(request, 'shop_cart.html', {
    #     'recipes': recipes,
    # })
    return redirect('purchase')


def download_purchase(request):
    content = ''
    if request.user.is_authenticated:
        ingredients = RecipeIngredient.objects.filter(
            recipe__in=Recipe.objects.filter(
                purchase__user=request.user
            )
        )
    else:
        # recipes = Recipe.objects.filter(purchase__user=request.user)
        recipes_ids = request.session.get('recipe_ids')
        if recipes_ids is not None:
            recipes = Recipe.objects.filter(pk__in=recipes_ids)
        ingredients = recipes.order_by('ingredient__title').values(
            'ingredient__title',
            'ingredient__dimension').annotate(
            total_count=Sum('counts__count'))
    # print(recipes)
    for ingredient in ingredients:
        ingredient_str = f'{ingredient["ingredient__title"]} - {ingredient["total_count"]} {ingredient["ingredient__dimension"]}'
        content += f'{ingredient_str}' + '\n'
    filename = 'recipe_ingredients.pdf'
    response = HttpResponse(content=content, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    buffer = BytesIO()
    MyFontObject = ttfonts.TTFont('Arial', 'arial.ttf')
    pdfmetrics.registerFont(MyFontObject)
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Arial", 9)
    p.drawString(260, 750, 'Список покупок:')
    x1 = 20
    y1 = 720
    for key in ingredients:
        p.drawString(x1, y1 - 12,
                     f'{key["ingredient__title"]} - {key["total_count"]} {key["ingredient__dimension"]}')
        y1 -= 20
        p.setTitle("Список покупок")
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


# @cache_page(20)
@login_required()
def follow_list(request):
    queryset = request.user.follower.all()
    # active_tags = get_active_tags(request)
    # if active_tags:
    #     queryset = filter_by_tags(queryset, active_tags)

    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    page = pagination(paginator, page_number)
    # tags = Tag.objects.all()
    return render(
        request,
        "follow.html",
        {
            "page": page,
            # "tags": tags,
            "paginator": paginator,
            # 'active_tags': active_tags,
        }
    )


# @cache_page(20)
@login_required()
def favorite_list(request):
    queryset = Recipe.objects.filter(favorite__user=request.user)
    active_tags = get_active_tags(request)
    if active_tags:
        queryset = services.filter_by_tags(queryset, active_tags)

    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    page = pagination(paginator, page_number)
    tags = Tag.objects.all()
    return render(
        request,
        "favorite.html",
        {
            "page": page,
            "tags": tags,
            "paginator": paginator,
            'active_tags': active_tags,
        }
    )
