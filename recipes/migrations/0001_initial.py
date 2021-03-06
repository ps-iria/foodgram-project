# Generated by Django 3.2 on 2021-05-05 10:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittle', models.CharField(max_length=250, unique=True, verbose_name='Название')),
                ('unit', models.CharField(max_length=250, verbose_name='Единицы измерения')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittle', models.CharField(max_length=250, unique=True, verbose_name='Название')),
                ('image', models.ImageField(blank=True, null=True, upload_to='recipes/', verbose_name='Изображение')),
                ('text', models.TextField(blank=True, max_length=500, verbose_name='Текстовое описание')),
                ('tag', models.CharField(choices=[('завтрак', 'завтрак'), ('обед', 'обед'), ('ужин', 'ужин')], max_length=7)),
                ('cook_time', models.PositiveIntegerField(verbose_name='Текстовое описание')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField()),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='Ингридиент'),
        ),
    ]
