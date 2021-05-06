from django.contrib import admin

from recipes.models import Recipe, RecipeIngredient, Ingredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    raw_id_fields = ('ingredient',)


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline, ]
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
    prepopulated_fields = {'slug': ('tittle',)}
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
