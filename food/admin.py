import models
from forms import IngredientForm, MealIngredientForm
from django.contrib import admin

# Register your models here.


class FoodAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super(FoodAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    exclude = ('user',)


class RecipePhotoAdmin(FoodAdmin):
    pass


admin.site.register(models.RecipePhoto, RecipePhotoAdmin)


class IngredientAdmin(FoodAdmin):
    form = IngredientForm
    fieldsets = (
        (None, {
            'fields': ('name', 'measurement')
        }),
        ('Nutrition Information', {
            'fields': (
                'calories', 'calories_from_fat', 'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol', 'sodium',
                'carbohydrate', 'fiber', 'sugars', 'protein', 'vitamin_a', 'vitamin_b', 'vitamin_c', 'vitamin_d',
                'calcium', 'iron', 'potassium')
        }),
    )


admin.site.register(models.Ingredient, IngredientAdmin)


class RecipeItemInline(admin.TabularInline):
    model = models.RecipeItem
    exclude = ('user', )
    extra = 1


class RecipePhotoInline(admin.TabularInline):
    model = models.RecipePhoto
    exclude = ('user', )
    extra = 1


class RecipeAdmin(FoodAdmin):
    exclude = (
        'user', 'calories', 'calories_from_fat', 'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol', 'sodium',
        'carbohydrate', 'fiber', 'sugars', 'protein', 'vitamin_a', 'vitamin_b', 'vitamin_c', 'vitamin_d', 'calcium',
        'iron',
        'potassium')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

    inlines = [RecipeItemInline, RecipePhotoInline]


admin.site.register(models.Recipe, RecipeAdmin)


class RecipeItemAdmin(FoodAdmin):
    pass


admin.site.register(models.RecipeItem, RecipeItemAdmin)


class MeasurementAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Measurement, MeasurementAdmin)


class MealCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.MealCategory, MealCategoryAdmin)


class TagAdmin(FoodAdmin):
    pass


admin.site.register(models.Tag, TagAdmin)


class MealIngredientAdmin(FoodAdmin):
    form = MealIngredientForm
    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
        ('Nutrition Information', {
            'fields': (
                'calories', 'calories_from_fat', 'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol', 'sodium',
                'carbohydrate', 'fiber', 'sugars', 'protein', 'vitamin_a', 'vitamin_b', 'vitamin_c', 'vitamin_d',
                'calcium',
                'iron', 'potassium')
        }),
    )


admin.site.register(models.MealIngredient, MealIngredientAdmin)


class MealItemInline(admin.TabularInline):
    model = models.MealItem
    exclude = ('user',)
    extra = 1


class MealAdmin(FoodAdmin):
    exclude = (
        'user', 'calories', 'calories_from_fat', 'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol', 'sodium',
        'carbohydrate', 'fiber', 'sugars', 'protein', 'vitamin_a', 'vitamin_b', 'vitamin_c', 'vitamin_d', 'calcium',
        'iron',
        'potassium')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()

    inlines = [MealItemInline]


admin.site.register(models.Meal, MealAdmin)


class MealItemAdmin(FoodAdmin):
    pass


admin.site.register(models.MealItem, MealItemAdmin)


class NutritionLogAdmin(FoodAdmin):
    exclude = (
        'user', 'calories', 'calories_from_fat', 'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol', 'sodium',
        'carbohydrate', 'fiber', 'sugars', 'protein', 'vitamin_a', 'vitamin_b', 'vitamin_c', 'vitamin_d', 'calcium',
        'iron',
        'potassium')


admin.site.register(models.NutritionLog, NutritionLogAdmin)


class NutritionProfileAdmin(FoodAdmin):
    pass


admin.site.register(models.NutritionProfile, NutritionProfileAdmin)
