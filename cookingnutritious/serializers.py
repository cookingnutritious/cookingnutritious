from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from rest_framework.relations import PrimaryKeyRelatedField
from food.models import (
    Measurement,
    Ingredient,
    Recipe,
    RecipeItem,
    RecipePhoto,
    MealCategory,
    MealItem,
    MealIngredient,
    Meal
)
from usda.models import Food


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class FoodGroupListingField(serializers.RelatedField):
    def to_native(self, value):
        return '%s' % value.description


class NutrientDataListingField(serializers.RelatedField):
    def to_native(self, value):
        return {
            ('%s' % value.nutrient.description): ('%f' % value.nutrient_value).rstrip('0').rstrip('.').lstrip('0'), }


class FoodSerializer(serializers.HyperlinkedModelSerializer):
    food_group = FoodGroupListingField()

    class Meta:
        model = Food
        fields = ('url', 'long_description', 'ndb_number')


class FoodDetailSerializer(serializers.HyperlinkedModelSerializer):
    nutrients = NutrientDataListingField(many=True)
    food_group = FoodGroupListingField()

    class Meta:
        model = Food
        fields = (
            'url', 'long_description', 'ndb_number', 'food_group', 'nutrients', 'short_description', 'common_name',
            'manufacturer_name', 'survey', 'refuse_description', 'refuse_percentage', 'scientific_name',
            'nitrogen_factor',
            'protein_factor', 'fat_factor', 'cho_factor')


class MeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Measurement
        fields = ('url', 'id', 'unit', 'gram_weight')


class MealCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MealCategory
        fields = ('url', 'name', 'id')


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'url', 'measurement', 'name', 'calories', 'calories_from_fat', 'total_fat', 'saturated_fat', 'trans_fat',
            'cholesterol', 'sodium', 'carbohydrate', 'fiber', 'sugars', 'protein', 'vitamin_a', 'vitamin_b',
            'vitamin_c',
            'vitamin_d', 'calcium', 'iron', 'potassium')


class RecipeItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecipeItem
        fields = ('url', 'recipe', 'ingredient', 'amount')


class RecipePhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecipePhoto
        fields = ('url', 'recipe', 'name', 'uri')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecipePhoto
        fields = ('name', )


class RecipeItemListingField(serializers.RelatedField):
    def to_native(self, value):
        return ('%f' % value.amount).rstrip('0').rstrip('.').lstrip('0') + \
            ' %s %s ' % (value.ingredient.measurement, value.ingredient.name)


class RecipePhotoListingField(serializers.RelatedField):
    def to_native(self, value):
        return '%s' % value.uri


class TagListingField(serializers.RelatedField):
    def to_native(self, value):
        return '%s' % value.name


class MealCategoryListingField(serializers.RelatedField):
    def to_native(self, value):
        return '%s' % value.name


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    recipe_items = RecipeItemListingField(many=True)
    recipe_photos = RecipePhotoListingField(many=True)
    tags = TagListingField(many=True)
    meal_category = MealCategoryListingField()

    class Meta:
        model = Recipe
        fields = (
            'url', 'name', 'instructions', 'prepare_time', 'cook_time', 'servings', 'serving_size', 'meal_category',
            'tags',
            'recipe_items', 'recipe_photos', 'calories', 'calories_from_fat', 'total_fat', 'saturated_fat', 'trans_fat',
            'cholesterol', 'sodium', 'carbohydrate', 'fiber', 'sugars', 'protein', 'vitamin_a', 'vitamin_b',
            'vitamin_c',
            'vitamin_d', 'calcium', 'iron', 'potassium')


class MealMeasurementListingField(serializers.RelatedField):
    def to_native(self, value):
        return '%s' % value.unit


class MealIngredientSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MealIngredient
        fields = (
            'url', 'id', 'name', 'calories', 'calories_from_fat', 'total_fat', 'saturated_fat', 'trans_fat',
            'cholesterol', 'sodium', 'carbohydrate', 'fiber', 'sugars', 'protein', 'vitamin_a', 'vitamin_b',
            'vitamin_c',
            'vitamin_d', 'calcium', 'iron', 'potassium')


class MealListingField(serializers.RelatedField):
    def to_native(self, value):
        return value.id


class MealItemListingField(serializers.RelatedField):
    def to_native(self, value):
        return ('%f' % value.amount).rstrip('0').rstrip('.').lstrip('0') + \
            ' %s %s ' % (value.measurement, value.ingredient.name)


class UserListingField(serializers.RelatedField):
    def to_native(self, value):
        return '%s' % value.id


class MealItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MealItem
        fields = ('url', 'id', 'measurement', 'meal', 'ingredient', 'amount')


class MealItemNestedSerializer(serializers.HyperlinkedModelSerializer):
    ingredient = MealIngredientSerializer()
    measurement = MeasurementSerializer()

    class Meta:
        model = MealItem
        fields = ('url', 'id', 'measurement', 'meal', 'ingredient', 'amount')


class MealCategoryNestedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = MealCategory
        fields = ('url', 'name', 'id')


class MealSerializer(serializers.HyperlinkedModelSerializer):
    meal_items = MealItemNestedSerializer(many=True)
    meal_category = PrimaryKeyRelatedField()

    class Meta:
        model = Meal
        fields = ('url', 'id', 'meal_category', 'day', 'meal_items', 'calories', 'calories_from_fat', 'total_fat',
                  'saturated_fat', 'trans_fat', 'cholesterol', 'sodium', 'carbohydrate', 'fiber', 'sugars', 'protein',
                  'vitamin_a', 'vitamin_b', 'vitamin_c', 'vitamin_d', 'calcium', 'iron', 'potassium')


class TokenSerializer(serializers.HyperlinkedModelSerializer):
    user = UserListingField()

    class Meta:
        model = Token
        depth = 1
        fields = ('key', 'user')


class NutritionSerializer(serializers.Serializer):
    pass
