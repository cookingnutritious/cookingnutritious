from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

class Measurement(models.Model):
    def __unicode__( self ):
        return self.unit
    unit = models.CharField(max_length=50)

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

class Ingredient(Nutrition):
    def __unicode__( self ):
        return ("%s (%s)" % (self.name, self.measurement))
    user = models.ForeignKey(User)   
    measurement = models.ForeignKey(Measurement)
    name = models.CharField(max_length=200)
    
class Recipe(Nutrition):
    def __unicode__( self ):
        return self.name

    def get_nutritional_information(self):
        recipe_items = RecipeItem.objects.filter(recipe=self)
        for item in recipe_items:
            self.calories += item.ingredient.calories
            self.calories_from_fat += item.ingredient.calories_from_fat
            self.total_fat += item.ingredient.total_fat
            self.saturated_fat += item.ingredient.saturated_fat
            self.trans_fat += item.ingredient.trans_fat
            self.cholesterol += item.ingredient.cholesterol
            self.sodium += item.ingredient.sodium
            self.carbohydrate += item.ingredient.carbohydrate
            self.fiber += item.ingredient.fiber
            self.sugars += item.ingredient.sugars
            self.protein += item.ingredient.protein
            self.vitamin_a += item.ingredient.vitamin_a
            self.vitamin_b += item.ingredient.vitamin_b
            self.vitamin_c += item.ingredient.vitamin_c
            self.vitamin_d += item.ingredient.vitamin_d
            self.calcium += item.ingredient.calcium
            self.iron += item.ingredient.iron
            self.potassium += item.ingredient.potassium
        self.calories = self.calories/self.servings
        self.calories_from_fat = self.calories_from_fat/self.servings
        self.total_fat = self.total_fat/self.servings
        self.trans_fat = self.trans_fat/self.servings
        self.cholesterol = self.cholesterol/self.servings
        self.sodium = self.sodium/self.servings
        self.carbohydrate = self.carbohydrate/self.servings
        self.fiber = self.fiber/self.servings
        self.sugars = self.sugars/self.servings
        self.protein = self.protein/self.servings
        self.vitamin_a = self.vitamin_a/self.servings
        self.vitamin_b = self.vitamin_b/self.servings
        self.vitamin_c = self.vitamin_c/self.servings
        self.vitamin_d = self.vitamin_d/self.servings
        self.calcium = self.calcium/self.servings
        self.iron = self.iron/self.servings
        self.potassium = self.potassium/self.servings
        return self
            
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    instructions = HTMLField()
    prepare_time = models.IntegerField(default=0)
    cook_time = models.IntegerField(default=0)
    servings = models.FloatField('Makes how many servings', default=1)
    serving_size = models.CharField(max_length=30)


class RecipeItem(models.Model):
    def __unicode__( self ):
        return ("%s - %s" % (self.recipe, self.ingredient))
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe, related_name='recipe_items')
    ingredient = models.ForeignKey(Ingredient)
    amount = models.FloatField(default=1)

class RecipePhoto(models.Model):
    def __unicode__( self ):
        return ("%s - %s" % (self.recipe, self.name))
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe, related_name='recipe_photos')
    name = models.CharField(max_length=30)
    uri = models.CharField(max_length=255)
