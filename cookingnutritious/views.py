from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from rest_framework import viewsets
from food.models import Measurement, Ingredient, Recipe, RecipeItem
from django.contrib.auth.models import User, Group
from cookingnutritious.serializers import UserSerializer, GroupSerializer, MeasurementSerializer, IngredientSerializer, RecipeSerializer, RecipeItemSerializer
from django.shortcuts import get_object_or_404

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

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    def get_queryset(self):
        user = self.request.user
        recipies = Recipe.objects.filter(user=user);
        for recipe in recipies:
            recipe = recipe.get_nutritional_information()
        return recipies
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup = self.kwargs.get(lookup_url_kwarg, None)
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        if lookup is not None:
            filter_kwargs = {self.lookup_field: lookup}
        elif pk is not None and self.lookup_field == 'pk':
            warnings.warn(
                PendingDeprecationWarning
            )
            filter_kwargs = {'pk': pk}
        elif slug is not None and self.lookup_field == 'pk':
            warnings.warn(
                PendingDeprecationWarning
            )
            filter_kwargs = {self.slug_field: slug}
        else:
            raise ImproperlyConfigured(
                (self.__class__.__name__, self.lookup_field)
            )

        obj = get_object_or_404(queryset, **filter_kwargs)
        obj.get_nutritional_information()
        self.check_object_permissions(self.request, obj)
        return obj

class RecipeItemViewSet(viewsets.ModelViewSet):
    queryset = RecipeItem.objects.all()
    serializer_class = RecipeItemSerializer
    def get_queryset(self):
        user = self.request.user
        return RecipeItem.objects.filter(user=user)

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    def get_queryset(self):
        user = self.request.user
        return Ingredient.objects.filter(user=user)

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
