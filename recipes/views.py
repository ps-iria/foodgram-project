from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, \
    InvalidPage
from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from pytils.translit import slugify
from django.views.decorators.cache import cache_page
from django.views.generic import DetailView, ListView

from recipes.forms import CreateRecipeForm
from recipes.models import Recipe, Ingredient, RecipeIngredient


# @cache_page(20)
def RecipeList(request):
    queryset = Recipe.objects.all()
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page = pagination(paginator, page_number)
    return render(
        request,
        "index.html",
        {
            "page": page,
            "paginator": paginator,
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


def RecipeNew(request):
    form = CreateRecipeForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(
            request,
            'new_recipe.html',
            {
                'form': form
            }
        )
    # save_recipe(request, form)
    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.slug = slugify(form.cleaned_data['title'])
    recipe.save()
    return redirect("index")


def get_ingredients(request):
    ingredients = {}
    for key, name in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = request.POST[
                f'valueIngredient_{num}'
            ]
    return ingredients


def save_recipe(request, form):
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.slug = slugify(request.title)
            recipe.save()

            objs = []
            ingredients = get_ingredients(request)
            for name, amount in ingredients.items():
                ingredient = get_object_or_404(Ingredient, name=name)
                objs.append(
                    RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        amount=amount
                    )
                )
            RecipeIngredient.objects.bulk_create(objs)
            form.save_m2m()
            return recipe

    except IntegrityError:
        raise HttpResponseBadRequest
