from django import template
from usda.forms import SearchUsdaForm
register = template.Library()

@register.inclusion_tag('cookingnutritious/search_usda.html')
def search_usda_form():
   return {
        'form': SearchUsdaForm(),
    }

