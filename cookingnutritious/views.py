from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from rest_framework import viewsets
from food.models import Measurement, Ingredient, Recipe, RecipeItem
from django.contrib.auth.models import User, Group
from cookingnutritious.serializers import UserSerializer, GroupSerializer, MeasurementSerializer, IngredientSerializer, RecipeSerializer, RecipeItemSerializer

# Create your views here.

def index(request):
    context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
    return render_to_response('cookingnutritious/index.html',
                             context_instance=context)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class RecipeItemViewSet(viewsets.ModelViewSet):
    queryset = RecipeItem.objects.all()
    serializer_class = RecipeItemSerializer
