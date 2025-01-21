from django.core.validators import RegexValidator

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        validators=[
            RegexValidator(regex=r'^[\w.@+-]+\Z')
        ],
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        db_index=True,
        validators=[
            RegexValidator(regex=r'^[\w.@+-]+\Z')
        ],
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
    )
    avatar = models.ImageField(
        verbose_name='Аватар пользователя',
        upload_to='users/',
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = 'id',

    def __str__(self):
        return self.username


class Subscription(models.Model):

    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'], name='unique_subscription'
            )
        ]

    def __str__(self):
        return f'{self.subscriber} {self.author}'
