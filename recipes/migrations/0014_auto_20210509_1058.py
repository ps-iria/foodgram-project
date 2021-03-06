# Generated by Django 3.2 on 2021-05-09 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_rename_slug_tag_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='numbers', to='recipes.ingredient'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='counts', to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(choices=[('Завтрак', 'Breakfast'), ('Обед', 'Lunch'), ('Ужин', 'Dinner')], max_length=50, unique=True, verbose_name='Название'),
        ),
    ]
