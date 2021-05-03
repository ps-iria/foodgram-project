from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username',
            'role',
            'email',
            'confirmation_code',
            'bio',
            'first_name',
            'last_name'
        )
        model = User
        extra_kwargs = {'username': {'required': True},
                        'email': {'required': True}
                        }
