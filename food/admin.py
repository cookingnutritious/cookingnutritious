import models
from django.contrib import admin

# Register your models here.

class MeasurementAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Measurement, MeasurementAdmin)

def ingredient_display_name(obj):
    return ("%s (%s)" % (obj.name, obj.measurement))
ingredient_display_name.short_description = 'Name'
class IngredientAdmin(admin.ModelAdmin):
    list_display = (ingredient_display_name,)

admin.site.register(models.Ingredient, IngredientAdmin)