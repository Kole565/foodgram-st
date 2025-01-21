import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from users.models import User, Subscription


class CustomImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='photo.' + ext)

        return super().to_internal_value(data)


class CustomUserSerializer(UserCreateSerializer):
    """For reading"""
    is_subscribed = serializers.SerializerMethodField()
    avatar = CustomImageField(use_url=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'avatar')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user

        if user.is_anonymous:
            return False

        return Subscription.objects.filter(subscriber=user, author=obj.id).exists()


class CustomCreateUserSerializer(CustomUserSerializer):
    """For creating"""
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password'
        )
        extra_kwargs = {'password': {'write_only': True}}


class CustomUserAvatarSerializer(serializers.ModelSerializer):
    avatar = CustomImageField(use_url=True)

    def validate(self, data):
        avatar = self.initial_data.get("avatar")
        if not avatar:
            raise serializers.ValidationError("Аватар не может быть пустым")

        return data

    class Meta:
        model = User
        fields = ('avatar',)
