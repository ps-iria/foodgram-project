"""
Фабрика для генерации рецепта для заполнения БД тестовыми данным
"""
import random
from random import choice

import factory
from factory import fuzzy
from slugify import UniqueSlugify

from users.factories import UserFactory
from . import models
from .models import Tag

COLOR = ["red", "blue", "green", "yellow", "purple", "orange", "white",
         "black"]
TAGS = ["Завтрак", "Обед", "Ужин"]


class RelatedObjectFactory(factory.Factory):
    FACTORY_FOR = models.Tag
    one = choice(TAGS)
    related = None


class BaseRecipeFactory(factory.django.DjangoModelFactory):
    """Factory that generates Recipes without Ingredients."""
    author = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=3)
    image = factory.django.ImageField(width=1000,
                                      color=factory.fuzzy.FuzzyChoice(COLOR))
    description = factory.Faker('text')
    # no ingredients
    cook_time = fuzzy.FuzzyInteger(10, 120)

    class Meta:
        model = models.Recipe

    @factory.lazy_attribute
    def slug(self):
        custom_slugify = UniqueSlugify()
        return custom_slugify(self.title)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        count_tags = fuzzy.FuzzyInteger(1, 3)
        tags = random.sample(tuple(Tag.objects.all()), count_tags.fuzz())
        self.tags.set(tags)


class RecipeIngredientFactory(factory.django.DjangoModelFactory):
    """Factory that generates Recipes with Ingredients."""
    recipe = factory.SubFactory(BaseRecipeFactory)
    count = fuzzy.FuzzyInteger(50, 500)

    class Meta:
        model = models.RecipeIngredient

    @factory.lazy_attribute
    def ingredient(self):
        return choice(models.Ingredient.objects.all())


class RecipeFactory(BaseRecipeFactory):
    """Factory that generates Recipes with 5 Ingredients."""

    ingredient_1 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
    ingredient_2 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
    ingredient_3 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
    ingredient_4 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
    ingredient_5 = factory.RelatedFactory(
        RecipeIngredientFactory,
        factory_related_name='recipe',
    )
