# Generated by Django 5.1.5 on 2025-01-29 14:13

import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Электронная почта"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        db_index=True,
                        max_length=150,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="(?!me\\b)(^[\\w.@+-]+\\Z)"
                            )
                        ],
                        verbose_name="Имя пользователя",
                    ),
                ),
                ("first_name", models.CharField(max_length=150, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=150, verbose_name="Фамилия")),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        upload_to="users/",
                        verbose_name="Аватар пользователя",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
                "ordering": ("username",),
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscriptions_where_author",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
                (
                    "subscriber",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscriptions_where_subscriber",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Подписчик",
                    ),
                ),
            ],
            options={
                "verbose_name": "Подписка",
                "verbose_name_plural": "Подписки",
                "ordering": ("author__username",),
                "constraints": [
                    models.UniqueConstraint(
                        fields=("subscriber", "author"), name="unique_subscription"
                    )
                ],
            },
        ),
    ]
