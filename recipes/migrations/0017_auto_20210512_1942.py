# Generated by Django 3.2 on 2021-05-12 12:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0016_alter_recipe_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='background_color',
            field=models.CharField(default='#000000', max_length=20, verbose_name='Цвет фона тега'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
    ]