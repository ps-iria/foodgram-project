from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

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
        verbose_name='Название рецепта',
        unique=True,
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата/Время создания",
        auto_now_add=True
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name='Изображение',
    )
    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Описание',
    )
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингридиенты',
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
        verbose_name='Время приготовления',
    )
    slug = models.SlugField(
        null=True,
        unique=True,
    )

    def __str__(self):
        return self.tittle

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('tittle',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
