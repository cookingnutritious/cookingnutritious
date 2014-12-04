from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from tinymce.models import HTMLField


def compose_nutritional_information(obj, collection):
        for item in collection:
            obj.calories += item.ingredient.calories * item.amount
            obj.calories_from_fat += item.ingredient.calories_from_fat * item.amount
            obj.total_fat += item.ingredient.total_fat * item.amount
            obj.saturated_fat += item.ingredient.saturated_fat * item.amount
            obj.trans_fat += item.ingredient.trans_fat * item.amount
            obj.cholesterol += item.ingredient.cholesterol * item.amount
            obj.sodium += item.ingredient.sodium * item.amount
            obj.carbohydrate += item.ingredient.carbohydrate * item.amount
            obj.fiber += item.ingredient.fiber * item.amount
            obj.sugars += item.ingredient.sugars * item.amount
            obj.protein += item.ingredient.protein * item.amount
            obj.vitamin_a += item.ingredient.vitamin_a * item.amount
            obj.vitamin_b += item.ingredient.vitamin_b * item.amount
            obj.vitamin_c += item.ingredient.vitamin_c * item.amount
            obj.vitamin_d += item.ingredient.vitamin_d * item.amount
            obj.calcium += item.ingredient.calcium * item.amount
            obj.iron += item.ingredient.iron * item.amount
            obj.potassium += item.ingredient.potassium * item.amount
        if hasattr(obj, 'servings'):
            obj.calories = round(obj.calories/obj.servings, 2)
            obj.calories_from_fat = round(obj.calories_from_fat/obj.servings, 2)
            obj.total_fat = round(obj.total_fat/obj.servings, 2)
            obj.saturated_fat = round(obj.saturated_fat/obj.servings, 2)
            obj.trans_fat = round(obj.trans_fat/obj.servings, 2)
            obj.cholesterol = round(obj.cholesterol/obj.servings, 2)
            obj.sodium = round(obj.sodium/obj.servings, 2)
            obj.carbohydrate = round(obj.carbohydrate/obj.servings, 2)
            obj.fiber = round(obj.fiber/obj.servings, 2)
            obj.sugars = round(obj.sugars/obj.servings, 2)
            obj.protein = round(obj.protein/obj.servings, 2)
            obj.vitamin_a = round(obj.vitamin_a/obj.servings, 2)
            obj.vitamin_b = round(obj.vitamin_b/obj.servings, 2)
            obj.vitamin_c = round(obj.vitamin_c/obj.servings, 2)
            obj.vitamin_d = round(obj.vitamin_d/obj.servings, 2)
            obj.calcium = round(obj.calcium/obj.servings, 2)
            obj.iron = round(obj.iron/obj.servings, 2)
            obj.potassium = round(obj.potassium/obj.servings, 2)


# Create your models here.
class MealCategory(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=30)


class Tag(models.Model):
    def __unicode__(self):
        return self.name
    user = models.ForeignKey(User) 
    name = models.CharField(max_length=30)


class Measurement(models.Model):
    def __unicode__(self):
        return self.unit
    unit = models.CharField(max_length=50)
    gram_weight = models.FloatField(default=0)


class Nutrition(models.Model):
    class Meta:
        abstract = True
    calories = models.FloatField('Calories per serving', default=0)
    calories_from_fat = models.FloatField('Calories from fat', default=0)
    total_fat = models.FloatField('Total fat', default=0)
    saturated_fat = models.FloatField('Saturated fat', default=0)
    trans_fat = models.FloatField('Trans fat', default=0)
    cholesterol = models.FloatField(default=0)
    sodium = models.FloatField(default=0)
    carbohydrate = models.FloatField('Total Carbohydrate', default=0)
    fiber = models.FloatField(default=0)
    sugars = models.FloatField(default=0)
    protein = models.FloatField(default=0)
    vitamin_a = models.FloatField('Vitamin A', default=0)
    vitamin_b = models.FloatField('Vitamin B', default=0)
    vitamin_c = models.FloatField('Vitamin C', default=0)
    vitamin_d = models.FloatField('Vitamin D', default=0)
    calcium = models.FloatField(default=0)
    iron = models.FloatField(default=0)
    potassium = models.FloatField(default=0)

    def get_field_names(self):
        return self._meta.get_all_field_names()


class Ingredient(Nutrition):
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.measurement)
    user = models.ForeignKey(User)
    measurement = models.ForeignKey(Measurement)
    name = models.CharField(max_length=200)
  
 
class Recipe(Nutrition):
    def __unicode__(self):
        return self.name    
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    instructions = HTMLField()
    prepare_time = models.IntegerField(default=0)
    cook_time = models.IntegerField(default=0)
    servings = models.FloatField('Makes how many servings', default=1)
    serving_size = models.CharField(max_length=30, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, null=True)
    meal_category = models.ForeignKey(MealCategory)


class RecipeItem(models.Model):
    def __unicode__(self):
        return "%s - %s" % (self.recipe, self.ingredient)
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe, related_name='recipe_items')
    ingredient = models.ForeignKey(Ingredient)
    amount = models.FloatField(default=1)


class RecipePhoto(models.Model):
    def __unicode__(self):
        return "%s - %s" % (self.recipe, self.name)
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe, related_name='recipe_photos')
    name = models.CharField(max_length=30)
    uri = models.CharField(max_length=255)


class Meal(Nutrition):
    def __unicode__(self):
        return "%s - %s" % (self.meal_category, self.day)
    user = models.ForeignKey(User)
    day = models.DateField("day", default=datetime.now)
    meal_category = models.ForeignKey(MealCategory, blank=False, null=False)


class MealIngredient(Nutrition):
    def __unicode__(self):
        return self.name
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)


class MealItem(models.Model):
    def __unicode__(self):
        return "%s " % self.ingredient
    measurement = models.ForeignKey(Measurement)
    user = models.ForeignKey(User)
    ingredient = models.ForeignKey(MealIngredient)
    amount = models.FloatField(default=1)
    meal = models.ForeignKey(Meal, related_name='meal_items')
