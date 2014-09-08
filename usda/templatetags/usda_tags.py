from django import template

from ..facts import NutritionFacts


register = template.Library()


@register.filter
def nutritionfacts(food):
    return NutritionFacts(food)


@register.filter
def withcalories(facts, calories):
    facts.calories = calories
    return facts
