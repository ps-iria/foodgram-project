from django.core.paginator import (
    Paginator,
    PageNotAnInteger,
    EmptyPage,
    InvalidPage
)
from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from slugify import UniqueSlugify

from recipes.models import Ingredient, RecipeIngredient, Tag

TAGS = ["Завтрак", "Обед", "Ужин"]


def get_active_tags(request):
    """Получить список активных тегов для фильтрации рецептов"""
    tags = set()
    if 'tags' in request.GET:
        tags = set(request.GET.getlist('tags'))
        tags.intersection_update(set(TAGS))
    return tags


def get_content(request, queryset):
    """Получить словарь с данными для страницы"""
    active_tags = get_active_tags(request)
    if active_tags:
        queryset = filter_by_tags(queryset, active_tags)

    paginator = Paginator(queryset, 6)
    page_number = request.GET.get('page')
    page = pagination(paginator, page_number)
    tags = Tag.objects.all()
    return {
        "page": page,
        "tags": tags,
        "paginator": paginator,
        'active_tags': active_tags,
    }


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


def filter_by_tags(recipes, tags):
    """Отфильтровать рецепты по тегам"""
    return recipes.filter(tags__title__in=tags).distinct()


def get_ingredients(request):
    """Получить список ингредиентов из формы"""
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
    """Получить список активных тегов для фильтрации рецептов"""
    try:
        with transaction.atomic():
            custom_slugify = UniqueSlugify()
            recipe = form.save(commit=False)
            recipe.author = request.user
            if recipe.slug is None:
                recipe.slug = custom_slugify(form.cleaned_data['title'])
            recipe.save()
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            objs = []
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
