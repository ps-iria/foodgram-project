# Generated by Django 3.2 on 2021-05-06 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_recipe_pub_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='text',
            new_name='description',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cook_time',
            field=models.PositiveIntegerField(verbose_name='Время приготовления'),
        ),
    ]