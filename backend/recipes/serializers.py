from rest_framework import serializers
from api.serializers import CustomUserSerializer

from .models import (
    Ingredient, IngredientInRecipe, Recipe, Favorite, ShoppingCart
)
from api.serializers import CustomImageField


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientInRecipeSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    ingredients = IngredientInRecipeSerializer(
        source='ingredient_list', many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart', 'name',
            'image', 'text', 'cooking_time'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()


class CreateIngredientsInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    @staticmethod
    def validate_amount(value):
        if value < 1:
            raise serializers.ValidationError(
                'Количество ингредиента должно быть больше 0!'
            )
        return value

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount')


class CreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = CreateIngredientsInRecipeSerializer(many=True)
    image = CustomImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'name',
            'image', 'text', 'cooking_time'
        )

    def to_representation(self, instance):
        serializer = RecipeSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        )
        return serializer.data

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                'Список ингредиентов не может быть пустым!'
            )

        ingredient_list = []

        for ingredient in ingredients:
            if ingredient['id'] in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиенты должны быть уникальными!'
                )
            if not Ingredient.objects.filter(id=ingredient['id']).exists():
                raise serializers.ValidationError(
                    'Ингредиент должен существовать!'
                )

            ingredient_list.append(ingredient['id'])

        return data

    def create_ingredients(self, ingredients, recipe):
        for element in ingredients:
            id = element['id']
            ingredient = Ingredient.objects.get(pk=id)
            amount = element['amount']
            IngredientInRecipe.objects.create(
                ingredient=ingredient, recipe=recipe, amount=amount
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')

        user = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data, author=user)
        self.create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        IngredientInRecipe.objects.filter(recipe=instance).delete()

        self.create_ingredients(validated_data.pop('ingredients'), instance)

        return super().update(instance, validated_data)


class CustomRecipeSerializer(serializers.ModelSerializer):
    """For list"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class AddFavoritesSerializer(serializers.ModelSerializer):
    image = CustomImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
