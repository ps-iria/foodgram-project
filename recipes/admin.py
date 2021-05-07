from django.contrib import admin

from recipes.forms import TagForm
from recipes.models import Recipe, RecipeIngredient, Ingredient, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    raw_id_fields = ('ingredient',)


# class RecipeTagInline(admin.TabularInline):
#     model = RecipeIngredient
#     extra = 1
#     raw_id_fields = ('ingredient',)


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline, ]
    list_display = (
        'pk',
        'title',
        'author',
        'slug',
    )
    search_fields = (
        'title',
    )
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'unit'

    )
    search_fields = (
        'title',
    )
    list_filter = (
        'unit',
    )
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    form = TagForm
    fieldsets = (
        (None, {
            'fields': ('title', 'display_name', 'color',)
            }),
        )

admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(Ingredient, IngredientAdmin)
