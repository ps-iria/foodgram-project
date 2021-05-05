from django.contrib import admin

from recipes.models import Recipe, RecipeIngredient, Ingredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'tittle',
        'author',
        'tag',
        'slug',
    )
    search_fields = (
        'tittle',
    )
    list_filter = (
        'tag',
    )
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'tittle',
        'unit'

    )
    search_fields = (
        'tittle',
    )
    list_filter = (
        'unit',
    )
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Ingredient, IngredientAdmin)
