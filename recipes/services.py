from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from pytils.translit import slugify

from recipes.models import Ingredient, RecipeIngredient


def get_ingredients(request):
    ingredients = {}
    for key, name in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = request.POST[
                f'valueIngredient_{num}'
            ]
    return ingredients


def check_ingredients_exist(ingredients):
    """Проверка на существование ингредиента в БД"""
    for ingredient in ingredients.keys():
        try:
            Ingredient.objects.get(title=ingredient)
        except Ingredient.DoesNotExist:
            return True
        return False


def check_ingredients(ingredients):
    """Проверка, что передан хотябы 1 ингредиент"""
    if len(ingredients) == 0:
        return True
    return False


def check_ingredients_value(ingredients):
    """Проверка на то, что количество всех ингредиентов больше 0"""
    for ing_amount in ingredients.values():
        if int(ing_amount) <= 0:
            return True
        return False


def validate_ingredients(form, ingredients):
    """Валидация ингредиентов"""
    if check_ingredients(ingredients):
        context = {'form': form,
                   'ingr_error': 'Введите как минимум 1 ингредиент'}
        return context

    if check_ingredients_exist(ingredients):
        context = {'form': form,
                   'ingr_error': 'Такого ингредиента пока нет в базе'}
        return context

    if check_ingredients_value(ingredients):
        context = {'form': form,
                   'ingr_error':
                       'Вы ввели отрицательное число ингредиентов'}
        return context


def save_recipe(request, form, ingredients):
    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            print(recipe.slug)
            if recipe.slug is None:
                recipe.slug = slugify(form.cleaned_data['title'])
            recipe.save()
            # if recipe.ingredient.exists():
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            objs = []
            ingredients = get_ingredients(request)
            for title, count in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=title)
                objs.append(
                    RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        count=count
                    )
                )
            RecipeIngredient.objects.bulk_create(objs)
            form.save_m2m()
            return recipe

    except IntegrityError:
        raise HttpResponseBadRequest
