from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from api.models import Follow, Favorite
from recipes.models import Ingredient, Recipe

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Ingredient


class FollowSerializer(serializers.ModelSerializer):
    id = SlugRelatedField(queryset=User.objects.all(),
                          slug_field='id',
                          source='author')

    user = User.pk

    class Meta:
        fields = ('id',)
        model = Follow


class FavoriteSerializer(serializers.ModelSerializer):
    id = SlugRelatedField(queryset=Recipe.objects.all(),
                          slug_field='id',
                          source='recipe')
    user = User.pk

    class Meta:
        fields = ('id',)
        model = Favorite
