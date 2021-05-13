from random import randint, sample

from django.core.management.base import BaseCommand

from api.models import Favorite
from users.factories import UserFactory

from recipes.factories import RecipeFactory
from recipes.models import Recipe, User


USERS = 100
MAX_RECIPES = 20
MAX_FAVORITES = 10


class Command(BaseCommand):
    """Custom `filldb` command.

    Django commands docs:
    https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/

    """
    help = 'Fill DB with sample data'

    def handle(self, *args, **options):
        users = UserFactory.create_batch(USERS)

        for user in users:
            for _ in range(randint(0, MAX_RECIPES)):
                RecipeFactory(author=user, tags=(0, 1, 2))

        for user in User.objects.all():
            # User cannot favorite his own recipes
            recipes = list(Recipe.objects.exclude(author=user))
            to_favorite = sample(recipes, k=randint(1, MAX_FAVORITES))
            Favorite.objects.bulk_create([
                Favorite(user=user, recipe=recipe) for recipe in to_favorite
            ])
