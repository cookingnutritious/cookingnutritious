from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Measurement(models.Model):
    def __unicode__( self ):
        return self.unit
    unit = models.CharField(max_length=50)

class Ingredient(models.Model):
    def __unicode__( self ):
        return self.name
    measurement = models.ForeignKey(Measurement)
    name = models.CharField(max_length=200)
    calories = models.IntegerField('Calories per serving')
    calories_from_fat = models.IntegerField('Calories from fat', default=0)
    total_fat = models.IntegerField('Total fat', default=0)
    saturated_fat = models.IntegerField('Saturated fat', default=0)
    trans_fat = models.IntegerField('Trans fat', default=0)
    cholesterol = models.IntegerField(default=0)
    sodium = models.IntegerField(default=0)
    carbohydrate = models.IntegerField('Total Carbohydrate', default=0)
    fiber = models.IntegerField(default=0)
    sugars = models.IntegerField(default=0)
    protein = models.IntegerField(default=0)
    vitamin_a = models.IntegerField('Vitamin A', default=0)
    vitamin_b = models.IntegerField('Vitamin B', default=0)
    vitamin_c = models.IntegerField('Vitamin C', default=0)
    vitamin_d = models.IntegerField('Vitamin D', default=0)
    calcium = models.IntegerField(default=0)
    iron = models.IntegerField(default=0)

class Recipe(models.Model):
    def __unicode__( self ):
        return self.name
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    instructions = models.TextField()
    prepare_time = models.IntegerField(default=0)
    cook_time = models.IntegerField(default=0)
    servings = models.IntegerField('Makes how many servings', default=1)

class RecipeItem(models.Model):
    def __unicode__( self ):
        return self.ingredient.name
    recipe = models.ForeignKey(Recipe, related_name='recipe_items')
    ingredient = models.ForeignKey(Ingredient)
    amount = models.IntegerField(default=1)
