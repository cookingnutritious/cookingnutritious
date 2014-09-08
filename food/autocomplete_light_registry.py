import autocomplete_light
from usda.models import Food

class FoodAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['long_description',]
    autocomplete_js_attributes={'placeholder': 'Search USDA database',}
    widget_js_attributes = { 'max_values': 100, }
    limit_choices = 1000;

autocomplete_light.register(Food, FoodAutocomplete)
