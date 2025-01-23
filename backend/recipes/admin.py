from django.contrib.admin import ModelAdmin, register
from recipes.models import Ingredient, IngredientInRecipe, Recipe
from users.models import Subscription

from .models import Favorite, ShoppingCart


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ("pk", "name", "measurement_unit")
    search_fields = ("name",)


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ("pk", "name", "author", "get_favorites")
    list_filter = ("author", "name")
    search_fields = ("name",)

    def get_favorites(self, obj):
        return obj.favorites.count()

    get_favorites.short_description = (
        "Количество добавлений рецепта в избранное"
    )


@register(IngredientInRecipe)
class IngredientInRecipe(ModelAdmin):
    list_display = ("pk", "recipe", "ingredient", "amount")


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ("pk", "user", "recipe")


@register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_display = ("pk", "subscriber", "author")
    search_fields = ("subscriber", "author")
    list_filter = ("subscriber", "author")


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ("pk", "user", "recipe")
