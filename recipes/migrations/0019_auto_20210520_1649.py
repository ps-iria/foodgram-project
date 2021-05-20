# Generated by Django 3.2.2 on 2021-05-20 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0018_remove_tag_background_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Название рецепта'),
        ),
    ]
