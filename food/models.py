from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from tinymce.models import HTMLField


def calorie_macro(macro, value):
    if macro is 'fat':
        return value*9
    else:
        return value*4


def calculate_nutrition(value, modifier):
    return round(((modifier / 100) * value), 2)


def compose_nutritional_information(obj, collection, member=None):
    # assemble list of nutrient field names for dynamic composition
    nutrients = Nutrition.get_field_names(obj)

    for item in collection:
        for field in nutrients:
            #member is optional parameter to specify a child property of collection item
            if member is not None:
                #only execute if the item has the property and value is a float
                if hasattr(getattr(item, member), field) and isinstance(getattr(getattr(item, member), field), float):
                    #assign the value times the amount specified
                    value = (getattr(getattr(item, member), field)) * item.amount
                    #if the measurement property is present calculate dynamic
                    #nutrition info based on measurement
                    if hasattr(item, 'measurement'):
                        value = calculate_nutrition(value, item.measurement.gram_weight)
                    value = round((value + getattr(obj, field)), 2)
                    setattr(obj, field, value)
            #usually this will be an additional composition of already composite items
            else:
                #only execute if the item has the property and value is a float
                if hasattr(item, field) and isinstance(getattr(item, field), float):
                    #assign the value times the amount specified
                    value = round((getattr(item, field) + getattr(obj, field)), 2)
                    setattr(obj, field, value)

    #calculates net carbohydrates (total carb - fiber)
    obj.net_carbohydrate = round((obj.carbohydrate - obj.fiber), 2)

    #calculates calories from macros based on dynamic formula
    obj.calories_from_protein = round(calorie_macro('protein', obj.protein), 2)
    obj.calories_from_carbohydrate = round(calorie_macro('carbohydrate', obj.carbohydrate), 2)
    obj.calories_from_fat = round(calorie_macro('fat', obj.total_fat), 2)
    obj.calories_from_net_carbohydrate = round(calorie_macro('net_carbohydrate', obj.net_carbohydrate), 2)

    #calcuates calories based on dynamic formula
    obj.calories = round((obj.calories_from_protein + obj.calories_from_carbohydrate + obj.calories_from_fat), 2)

    #if the servings property is present calculate the average values based on servings
    if hasattr(obj, 'servings'):
        for field in nutrients:
            value = round(getattr(obj, field) / obj.servings, 2)
            setattr(obj, field, value)


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
    calories_from_protein = models.FloatField('Calories from protein', default=0)
    calories_from_carbohydrate = models.FloatField('Calories from carbohydrate', default=0)
    calories_from_net_carbohydrate = models.FloatField('Calories from net carbohydrate', default=0)
    net_carbohydrate = models.FloatField('Net carbohydrate', default=0)
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


class NutritionLog(Nutrition):
    def __unicode__(self):
        return "%s - %s : %s" % (self.user, self.day, ('%f' % self.weight).rstrip('0').rstrip('.'))
    user = models.ForeignKey(User)
    day = models.DateField("day", default=datetime.now)
    weight = models.FloatField(default=0)


class NutritionProfile(models.Model):
    def __unicode__(self):
        return "%s - %s" % (self.user, self.day)
    user = models.ForeignKey(User)
    day = models.DateField("day", default=datetime.now)
    target_calories = models.FloatField(default=0)
    target_protein = models.FloatField(default=0)
    target_carbohydrate = models.FloatField(default=0)
    target_fat = models.FloatField(default=0)
    target_fiber = models.FloatField(default=0)
