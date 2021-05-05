from django.core.management.base import BaseCommand, CommandError
from recipes.models import Ingredient
import csv
from foodgram.settings import BASE_DIR
import os

CSV_FILE_PATH = os.path.join(BASE_DIR, 'ingredients.csv')


class Command(BaseCommand):
    help = 'Загрузка ингридиентов'

    def handle(self, *args, **options):
        with open(CSV_FILE_PATH, encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                tittle, unit = row
                Ingredient.objects.get_or_create(tittle=tittle, unit=unit)
