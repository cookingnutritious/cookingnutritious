from django import forms
import autocomplete_light
from models import Ingredient, MealIngredient, Measurement
from usda.models import Food
from django.core.urlresolvers import reverse_lazy

class IngredientForm(forms.ModelForm):
    urlt = reverse_lazy('usda-search', args=['__long_description__', ])
    urlm = reverse_lazy('measurement-list')
    name = forms.CharField(
        widget=autocomplete_light.TextWidget('FoodAutocomplete', 
                                              attrs={
                                                  'data-url-template': urlt
                                                }
                                              ))
    measurement = forms.ModelChoiceField(queryset = Measurement.objects.all(),
        widget=forms.Select(attrs={'data-measurement-endpoint': urlm}))

    class Meta:
        model = Ingredient


class MealIngredientForm(forms.ModelForm):
    urlt = reverse_lazy('usda-search', args=['__long_description__', ])
    name = forms.CharField(
        widget=autocomplete_light.TextWidget('FoodAutocomplete',
                                              attrs={
                                                  'data-url-template': urlt
                                                }
                                              ))

    class Meta:
        model = MealIngredient

