from django import forms
from django.forms.widgets import TextInput

from recipes.models import Recipe, Tag


class CreateRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = (
            'author',
            'slug'
        )
        fields = '__all__'


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }
