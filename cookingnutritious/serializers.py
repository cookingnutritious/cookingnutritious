from rest_framework import serializers
from django.contrib.auth.models import User, Group
from food.models import Measurement, Ingredient, Recipe, RecipeItem, RecipePhoto, MealCategory
from usda.models import Food, NutrientData, Nutrient

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
        return ('%s') % (value.description)

class NutrientDataListingField(serializers.RelatedField):
    def to_native(self, value):
        return {('%s' % value.nutrient.description) : ('%f' % value.nutrient_value).rstrip('0').rstrip('.').lstrip('0'), }

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
        fields = ('url', 'long_description', 'ndb_number', 'food_group', 'nutrients', 'short_description', 'common_name', 'manufacturer_name', 'survey', 'refuse_description', 'refuse_percentage', 'scientific_name', 'nitrogen_factor', 'protein_factor', 'fat_factor', 'cho_factor' )

class MeasurementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Measurement
        fields = ('url', 'unit', 'gram_weight')

class MealCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MealCategory
        fields = ('name',)

class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('url', 'measurement', 'name', 'calories', 'calories_from_fat', 'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol', 'sodium', 'carbohydrate', 'fiber', 'sugars', 'protein', 'vitamin_a', 'vitamin_b', 'vitamin_c', 'vitamin_d', 'calcium', 'iron', 'potassium')

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
        return ('%f' % value.amount).rstrip('0').rstrip('.').lstrip('0') + (' %s %s ') % (value.ingredient.measurement, value.ingredient.name)

class RecipePhotoListingField(serializers.RelatedField):
    def to_native(self, value):
        return ('%s') % (value.uri)

class TagListingField(serializers.RelatedField):
    def to_native(self, value):
        return ('%s') % (value.name)

class MealCategoryListingField(serializers.RelatedField):
    def to_native(self, value):
        return ('%s') % (value.name)

class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    recipe_items = RecipeItemListingField(many=True)
    recipe_photos = RecipePhotoListingField(many=True)
    tags = TagListingField(many=True)
    meal_category = MealCategoryListingField()
    class Meta:
        model = Recipe
        fields = ('url', 'name', 'instructions', 'prepare_time', 'cook_time', 'servings', 'serving_size', 'meal_category', 'tags', 'recipe_items', 'recipe_photos', 'calories', 'calories_from_fat', 'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol', 'sodium', 'carbohydrate', 'fiber', 'sugars', 'protein', 'vitamin_a', 'vitamin_b', 'vitamin_c', 'vitamin_d', 'calcium', 'iron', 'potassium')
