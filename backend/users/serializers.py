from rest_framework import serializers

from api.serializers import CustomUserSerializer
from recipes.serializers import CustomRecipeSerializer
from users.models import Subscription, User


class SubscriptionSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField(
        read_only=True, method_name="get_recipes"
    )
    recipes_count = serializers.ReadOnlyField(source="recipes.count")

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
            "avatar",
        )

    def get_recipes(self, obj):
        request = self.context.get("request")
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get("recipes_limit")

        if recipes_limit:
            try:
                recipes = recipes[: int(recipes_limit)]
            except ValueError:
                pass

        return CustomRecipeSerializer(
            recipes, context={"request": request}, many=True
        ).data
