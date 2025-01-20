from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from .serializers import CustomUserSerializer, CustomUserAvatarSerializer
from users.serializers import SubscriptionSerializer
from users.models import User, Subscription


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(AllowAny,),
        url_path='me',
        url_name='me',
    )
    def me(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = CustomUserSerializer(
            request.user, context={'request': request}
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=('put', 'delete'),
        permission_classes=(IsAuthenticated,),
        url_path='avatar',
        url_name='avatar',
    )
    def avatar(self, request, id):
        user = request.user

        serializer = CustomUserAvatarSerializer(
            user, context={'request': request}
        )

        if request.method == 'PUT':
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated, ),
        url_path='subscriptions',
        url_name='subscriptions',
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(follow__user=self.request.subscriber)
        if queryset:
            pages = self.paginate_queryset(queryset)
            serializer = SubscriptionSerializer(
                pages, many=True,
                context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        return Response('Вы ни на кого не подписаны.',
                        status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated,),
        url_path='subscribe',
        url_name='subscribe',
    )
    def subscribe(self, request, id):
        subscriber = request.user
        author = get_object_or_404(User, id=id)
        change_subscription_status = Subscription.objects.filter(
            subscriber=subscriber.id, author=author.id
        )
        if request.method == 'POST':
            if subscriber == author:
                return Response('Вы пытаетесь подписаться на себя!!',
                                status=status.HTTP_400_BAD_REQUEST)
            if change_subscription_status.exists():
                return Response(f'Вы теперь подписаны на {author}',
                                status=status.HTTP_400_BAD_REQUEST)
            subscribe = Subscription.objects.create(
                subscriber=subscriber,
                author=author
            )
            subscribe.save()

            serializer = CustomUserSerializer(
                author, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if change_subscription_status.exists():
            change_subscription_status.delete()
            return Response(f'Вы отписались от {author}',
                            status=status.HTTP_204_NO_CONTENT)
        return Response(
            f'Вы не подписаны на {author}',
            status=status.HTTP_400_BAD_REQUEST
        )
