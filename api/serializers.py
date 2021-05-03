from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class GetTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(max_length=255, required=True)


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=30,
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
