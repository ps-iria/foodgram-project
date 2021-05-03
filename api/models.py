from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRoles(models.TextChoices):
    GUEST = 'guest'
    USER = 'user'
    ADMIN = 'admin'


class User(AbstractUser):
    role = models.CharField(
        max_length=10,
        choices=UserRoles.choices,
        default=UserRoles.USER,
        verbose_name='Роль пользователя',
    )
    email = models.EmailField(
        max_length=128,
        blank=False,
        unique=True,
        verbose_name='Адрес электронной почты',
        db_index=True,
    )
    username = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        verbose_name='Логин',
    )
    first_name = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Фамилия',
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='О себе',
    )
    confirmation_code = models.CharField(
        max_length=255,
        unique=True,
        editable=False,
        null=True,
        blank=True
    )

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN or self.is_superuser

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
