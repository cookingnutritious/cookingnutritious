from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Measurement(models.Model):
    def __unicode__( self ):
        return self.unit
    unit = models.CharField(max_length=50)

class Ingredient(models.Model):
    def __unicode__( self ):
        return ("%s (%s)" % (self.name, self.measurement))
    user = models.ForeignKey(User)   
    measurement = models.ForeignKey(Measurement)
    name = models.CharField(max_length=200)
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

class Recipe(models.Model):
    def __unicode__( self ):
        return self.name
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    instructions = models.TextField()
    prepare_time = models.IntegerField(default=0)
    cook_time = models.IntegerField(default=0)
    servings = models.FloatField('Makes how many servings', default=1)

class RecipeItem(models.Model):
    def __unicode__( self ):
        return ("%s - %s" % (self.recipe, self.ingredient))
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe, related_name='recipe_items')
    ingredient = models.ForeignKey(Ingredient)
    amount = models.FloatField(default=1)
