from django import forms

from recipes.models import Recipe


class CreateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = (
            'author',
            'slug'
        )
        fields = '__all__'
