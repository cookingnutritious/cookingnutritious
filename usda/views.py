from django.template import RequestContext, loader
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response
from usda.models import Food, NutrientData


class FoodListView(ListView):

    model = Food

    def get_context_data(self, **kwargs):
        context = super(FoodListView, self).get_context_data(**kwargs)
        return context

class FoodDetailView(DetailView):

    model = Food

    def get_context_data(self, **kwargs):
        context = super(FoodDetailView, self).get_context_data(**kwargs)
        context['nutrient_data'] = NutrientData.objects.filter(food=context['object'])
        return context

