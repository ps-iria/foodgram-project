from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    tittle = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    unit = models.CharField(
        max_length=250,
        verbose_name='Единицы измерения',
    )

    def __str__(self):
        return f'{self.tittle}, {self.unit}'

    class Meta:
        ordering = ('tittle',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    tittle = models.CharField(
        max_length=250,
        verbose_name='Название',
        unique=True,
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name='Изображение',
    )
    text = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Текстовое описание',
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингридиент',
    )
    TAGS = [
            ('завтрак', 'завтрак'),
            ('обед', 'обед'),
            ('ужин', 'ужин'),
        ]
    tag = models.CharField(
        max_length=7,
        choices=TAGS,
    )
    cook_time = models.PositiveIntegerField(
        verbose_name='Текстовое описание',
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
    )

    def __str__(self):
        return self.tittle

    class Meta:
        ordering = ('tittle',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
