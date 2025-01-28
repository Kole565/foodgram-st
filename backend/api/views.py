from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response

from api.serializers import CustomUserAvatarSerializer, CustomUserSerializer
from users.models import Subscription, User
from users.serializers import SubscriptionSerializer


class UserProfileViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
        url_path="me",
        url_name="me",
    )
    def me(self, request):
        serializer = CustomUserSerializer(
            request.user, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        detail=True,
        methods=("put", "delete"),
        permission_classes=(IsAuthenticated,),
        url_path="avatar",
        url_name="avatar",
    )
    def avatar(self, request, id):
        if request.method == "PUT":
            return self.create_avatar(request)
        return self.delete_avatar(request)

    def create_avatar(self, request):
        serializer = CustomUserAvatarSerializer(
            request.user, data=request.data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete_avatar(self, request):
        user = request.user
        if user.avatar:
            user.avatar.delete()
            user.avatar = None
            user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=("get",),
        permission_classes=(IsAuthenticated,),
        url_path="subscriptions",
        url_name="subscriptions",
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(author__subscriber=self.request.user)

        if queryset:
            pages = self.paginate_queryset(queryset)
            serializer = SubscriptionSerializer(
                pages, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        return Response(
            "Вы ни на кого не подписаны.", status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=True,
        methods=("post", "delete"),
        permission_classes=(IsAuthenticated,),
        url_path="subscribe",
        url_name="subscribe",
    )
    def subscribe(self, request, id):
        subscriber = request.user
        author = get_object_or_404(User, id=id)
        change_subscription_status = Subscription.objects.filter(
            subscriber=subscriber.id, author=author.id
        )
        if request.method == "POST":
            if subscriber == author:
                return Response(
                    "Вы пытаетесь подписаться на себя!!",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if change_subscription_status.exists():
                return Response(
                    f"Вы теперь подписаны на {author}",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscribe = Subscription.objects.create(
                subscriber=subscriber, author=author
            )
            subscribe.save()

            serializer = SubscriptionSerializer(
                request.user, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if change_subscription_status.exists():
            change_subscription_status.delete()
            return Response(
                f"Вы отписались от {author}", status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            f"Вы не подписаны на {author}", status=status.HTTP_400_BAD_REQUEST
        )
