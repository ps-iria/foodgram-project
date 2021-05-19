from django.contrib import admin
from django.utils.safestring import mark_safe

from recipes.forms import TagForm
from recipes.models import Recipe, RecipeIngredient, Ingredient, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline, ]
    list_display = (
        'pk',
        'title',
        'author',
        'slug',
    )
    list_filter = (
        'title',
    )
    readonly_fields = ['preview']
    search_fields = (
        'title',
    )
    prepopulated_fields = {'slug': ('title',)}
    empty_value_display = '-пусто-'

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="100">')


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'dimension'
    )
    search_fields = (
        'title',
    )
    list_filter = (
        'dimension',
        'title',
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
admin.site.register(Ingredient, IngredientAdmin)
