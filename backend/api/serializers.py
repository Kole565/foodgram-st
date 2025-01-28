from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from api.fields import Bit64ImageField
from users.models import Subscription, User


class CustomUserSerializer(UserCreateSerializer):
    """For reading"""

    is_subscribed = serializers.SerializerMethodField()
    avatar = Bit64ImageField(use_url=True)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "avatar",
        )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user

        if not user.is_authenticated:
            return False

        return Subscription.objects.filter(
            subscriber=user, author=obj.id
        ).exists()


class CustomCreateUserSerializer(CustomUserSerializer):
    """For creating"""

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}


class CustomUserAvatarSerializer(serializers.ModelSerializer):
    avatar = Bit64ImageField(use_url=True)

    class Meta:
        model = User
        fields = ("avatar",)

    def validate(self, data):
        avatar = self.initial_data.get("avatar")
        if not avatar:
            raise serializers.ValidationError("Аватар не может быть пустым")

        return data
