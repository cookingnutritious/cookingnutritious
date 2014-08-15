from rest_framework import serializers
from django.contrib.auth.models import User, Group
from food.models import Measurement, Ingredient, Recipe, RecipeItem

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class MeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Measurement

class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient

class RecipeItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecipeItem

class RecipeItemListingField(serializers.RelatedField):
    def to_native(self, value):
        return '%d %s %s' % (value.amount, value.ingredient.measurement, value.ingredient.name)

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    recipe_items = RecipeItemListingField(many=True)
    class Meta:
        model = Recipe
        fields = ('user', 'name', 'instructions', 'prepare_time', 'cook_time', 'servings', 'recipe_items')
