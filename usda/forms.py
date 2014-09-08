from django import forms
import autocomplete_light
from usda.models import Food

class SearchUsdaForm(forms.ModelForm):
    long_description = forms.ModelChoiceField(Food.objects.all(),
        widget=autocomplete_light.TextWidget('FoodAutocomplete'),
    )

    class Meta:
        model = Food
        fields = ('long_description', )
