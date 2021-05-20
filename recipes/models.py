from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    dimension = models.CharField(
        max_length=250,
        verbose_name='Единицы измерения',
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return f'{self.title}, {self.dimension}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название рецепта',
        unique=False,
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
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингридиенты',
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name="recipes",
        verbose_name="Теги",
    )
    cook_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
    )
    slug = models.SlugField(
        null=True,
        unique=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'recipe_slug': self.slug})


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="counts",
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="numbers",
    )
    count = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.ingredient} - {self.count}'


class Tag(models.Model):
    class Meal(models.TextChoices):
        BREAKFAST = "Завтрак"
        LUNCH = "Обед"
        DINNER = "Ужин"

    title = models.CharField(
        verbose_name="Название",
        max_length=50,
        choices=Meal.choices,
        unique=True
    )
    display_name = models.CharField(
        verbose_name="Имя тега в шаблоне",
        max_length=20,
    )
    color = models.CharField(
        verbose_name="Цвет тега",
        max_length=20,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.display_name
