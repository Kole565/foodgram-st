from djoser.views import UserViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
)
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from .serializers import CustomUserSerializer, CustomUserAvatarSerializer
from users.models import User


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
