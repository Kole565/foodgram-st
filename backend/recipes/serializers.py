from rest_framework import serializers
from django.shortcuts import get_object_or_404

from api.fields import Bit64ImageField
from api.serializers import UserProfileSerializer
from foodgram.constants import *
from recipes.models import (
    Favorite, Ingredient, IngredientInRecipe, Recipe, ShoppingCart
)


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="ingredient.id")
    name = serializers.CharField(source="ingredient.name")
    measurement_unit = serializers.CharField(
        source="ingredient.measurement_unit"
    )
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit", "amount")


class ShortIngredientsSerializer(serializers.ModelSerializer):
    """Serialize ingredients without IngredientInRecipe fields."""
    id = serializers.IntegerField()
    name = serializers.CharField()
    measurement_unit = serializers.CharField()

    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class RecipeSerializer(serializers.ModelSerializer):
    author = UserProfileSerializer()
    ingredients = IngredientSerializer(
        source="recipe_ingredientinrecipe", many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if (
            request is not None
            and request.user.is_authenticated
            and request.user.favorites.filter(pk=obj.id).exists()
        ):
            return True
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if (
            request is not None
            and request.user.is_authenticated
            and request.user.shopping_carts.filter(pk=obj.id).exists()
        ):
            return True
        return False


class CreateShortIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ("id", "amount")

    def validate_id(self, id):
        return get_object_or_404(Ingredient, id=id).id

    def validate_amount(self, value):
        if value < INGREDIENT_MIN_AMOUNT_IN_RECIPE:
            raise serializers.ValidationError(
                "Количество ингредиента должно быть больше {}!".format(
                    INGREDIENT_MIN_AMOUNT_IN_RECIPE - 1
                )
            )
        return value


class CreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = CreateShortIngredientsSerializer(many=True)
    image = Bit64ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = (
            "ingredients", "name", "image", "name", "text", "cooking_time"
        )

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance, context={"request": self.context.get("request")}
        )
        return serializer.data

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                "Список ингредиентов не может быть пустым!"
            )

        ingredient_list = []

        for ingredient in ingredients:
            if ingredient["id"] in ingredient_list:
                raise serializers.ValidationError(
                    "Ингредиенты должны быть уникальными!"
                )
            if not Ingredient.objects.filter(id=ingredient["id"]).exists():
                raise serializers.ValidationError(
                    "Ингредиент должен существовать!"
                )

            ingredient_list.append(ingredient["id"])

        return ingredients

    def create_ingredients(self, ingredients, recipe):
        for element in ingredients:
            id = element["id"]
            ingredient = Ingredient.objects.get(pk=id)
            amount = element["amount"]
            IngredientInRecipe.objects.create(
                ingredient=ingredient, recipe=recipe, amount=amount
            )

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")

        user = self.context.get("request").user
        recipe = Recipe.objects.create(**validated_data, author=user)
        self.create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        IngredientInRecipe.objects.filter(recipe=instance).delete()

        self.create_ingredients(validated_data.pop("ingredients"), instance)

        return super().update(instance, validated_data)


class ShortRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ("id", "name", "image", "cooking_time")


class UserRecipeRelationSerializer:

    class Meta:
        fields = ("user", "recipe")

    def to_representation(self, instance):
        serializer = ShortRecipeSerializer(instance.recipe)
        return serializer.data


class FavoriteSerializer(
    UserRecipeRelationSerializer, serializers.ModelSerializer
):

    class Meta(UserRecipeRelationSerializer.Meta):
        model = Favorite


class ShoppingCartSerializer(
    UserRecipeRelationSerializer, serializers.ModelSerializer
):

    class Meta(UserRecipeRelationSerializer.Meta):
        model = ShoppingCart
