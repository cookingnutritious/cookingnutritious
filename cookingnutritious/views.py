from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.views.decorators.cache import cache_control
from django.db.models import Q
from rest_framework import viewsets, views
from rest_framework.response import Response
from food.models import Measurement, Ingredient, Recipe, RecipeItem, RecipePhoto, MealCategory, Tag, compose_nutritional_information
from usda.models import Food 
from django.contrib.auth.models import User, Group
from cookingnutritious.serializers import UserSerializer, GroupSerializer, MeasurementSerializer, IngredientSerializer, RecipeSerializer, RecipeItemSerializer, RecipePhotoSerializer, MealCategorySerializer, TagSerializer, FoodSerializer, FoodDetailSerializer
from django.shortcuts import get_object_or_404
from rest_framework_extensions.mixins import DetailSerializerMixin
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework_extensions.etag.mixins import ETAGMixin 
from rest_framework_extensions.cache.decorators import cache_response
from rest_framework_extensions.etag.decorators import etag
from rest_framework_extensions.key_constructor.constructors import (
    KeyConstructor
)
from rest_framework_extensions.key_constructor import bits
import operator

class CookingNutritiousKeyConstructor(KeyConstructor):
    unique_view_id = bits.UniqueViewIdKeyBit()
    language = bits.LanguageKeyBit()
    format = bits.FormatKeyBit()

class CookingNutritiousRetrieveKeyConstructor(CookingNutritiousKeyConstructor):
    retrieve_sql_query = bits.RetrieveSqlQueryKeyBit()

class CookingNutritiousListKeyConstructor(CookingNutritiousKeyConstructor):
    list_sql_query = bits.ListSqlQueryKeyBit()

class RecipeListKeyConstructor(CookingNutritiousListKeyConstructor):
    user = bits.UserKeyBit()

class RecipeRetrieveKeyConstructor(CookingNutritiousRetrieveKeyConstructor):
    user = bits.UserKeyBit()

# Create your views here.
def index(request):
    context = RequestContext(request,
                           {'request': request,
                            'user': request.user})
    return render_to_response('cookingnutritious/index.html',
                             context_instance=context)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    
class FoodViewSet(DetailSerializerMixin, ETAGMixin, CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = FoodSerializer
    serializer_detail_class = FoodDetailSerializer
    queryset = Food.objects.all()
    retrieve_key_constructor_func = CookingNutritiousRetrieveKeyConstructor(memoize_for_request=True)
    @cache_control(private=True,max_age=31536000)
    @etag(retrieve_key_constructor_func)
    @cache_response(31536000, key_func=retrieve_key_constructor_func)
    def retrieve(self, request, *args, **kwargs):
        return super(FoodViewSet, self).retrieve(request, *args, **kwargs)
    list_key_constructor_func = CookingNutritiousListKeyConstructor(memoize_for_request=True)
    @cache_control(private=True,max_age=31536000)
    @etag(list_key_constructor_func)
    @cache_response(31536000, key_func=list_key_constructor_func)
    def list(self, request, *args, **kwargs):
        return super(FoodViewSet, self).list(request, *args, **kwargs)

class FoodSearchViewSet(DetailSerializerMixin, ETAGMixin, CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = FoodSerializer
    serializer_detail_class = FoodDetailSerializer
    queryset = Food.objects.all()
    lookup_field = 'long_description'
    def get_search_terms(self):
        list = self.kwargs['long_description'].replace('_', ' ').replace('XX', '\'').replace('YY', '\"').replace('ZZ', '/').split(' ')
        return reduce(operator.and_, (Q(long_description__contains=x) for x in list))
    def get_queryset(self, is_for_detail=False):
        terms = self.get_search_terms()
        return Food.objects.all().filter(terms)
    list_key_constructor_func = CookingNutritiousListKeyConstructor(memoize_for_request=True)
    @cache_control(private=True,max_age=31536000)
    @etag(list_key_constructor_func)
    @cache_response(31536000, key_func=list_key_constructor_func)
    def list(self, request, *args, **kwargs):
        terms = self.get_search_terms()
        result_count = Food.objects.all().filter(terms).count()
        if result_count > 1:
            return super(FoodSearchViewSet, self).list(request, *args, **kwargs)
        else:
            return self.retrieve(request, *args, **kwargs)
    retrieve_key_constructor_func = CookingNutritiousRetrieveKeyConstructor(memoize_for_request=True)
    @cache_control(private=True,max_age=31536000)
    @etag(retrieve_key_constructor_func)
    @cache_response(31536000, key_func=retrieve_key_constructor_func)
    def retrieve(self, request, *args, **kwargs):
        terms = self.get_search_terms()
        object = Food.objects.all().filter(terms)
        serializer = FoodDetailSerializer(object, context={'request': request})
        return Response(serializer.data)

def recipe_list_cache_key(view_instance, view_method, 
                        request, args, kwargs):
    return '.'.join([
        'recipes',
        get_format(request)
    ])

def recipe_detail_cache_key(view_instance, view_method, 
                        request, args, kwargs):
    return '.'.join([
        'recipes',
        kwargs['pk'],
        get_format(request)
    ])


class RecipeViewSet(DetailSerializerMixin, ETAGMixin, CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    serializer_detail_class = RecipeSerializer
    def get_queryset(self):
        user = self.request.user
        recipes = Recipe.objects.filter(user=user);
        for recipe in recipes:
            recipe_items = RecipeItem.objects.filter(recipe=recipe)
            recipe = compose_nutritional_information(recipe, recipe_items)
        return recipes
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
        recipe_items = RecipeItem.objects.filter(recipe=obj)
        obj = compose_nutritional_information(obj, recipe_items)
        self.check_object_permissions(self.request, obj)
        return obj
    retrieve_key_constructor_func = RecipeRetrieveKeyConstructor(memoize_for_request=True)
    @cache_control(private=True,max_age=7200)
    @etag(retrieve_key_constructor_func)
    @cache_response(60 * 2, key_func=retrieve_key_constructor_func)
    def retrieve(self, request, *args, **kwargs):
        return super(RecipeViewSet, self).retrieve(request, *args, **kwargs)
    list_key_constructor_func = RecipeListKeyConstructor(memoize_for_request=True)
    @cache_control(private=True,max_age=7200)
    @etag(list_key_constructor_func)
    @cache_response(60 * 2, key_func=list_key_constructor_func)
    def list(self, request, *args, **kwargs):
        return super(RecipeViewSet, self).list(request, *args, **kwargs)

class RecipeItemViewSet(viewsets.ModelViewSet):
    queryset = RecipeItem.objects.all()
    serializer_class = RecipeItemSerializer
    def get_queryset(self):
        user = self.request.user
        return RecipeItem.objects.filter(user=user)

class TagViewSet(viewsets.ModelViewSet):
    queryset = RecipeItem.objects.all()
    serializer_class = TagSerializer
    def get_queryset(self):
        user = self.request.user
        return Tag.objects.filter(user=user)

class RecipePhotoViewSet(viewsets.ModelViewSet):
    queryset = RecipePhoto.objects.all()
    serializer_class = RecipePhotoSerializer
    def get_queryset(self):
        user = self.request.user
        return RecipePhoto.objects.filter(user=user)

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    def get_queryset(self):
        user = self.request.user
        return Ingredient.objects.filter(user=user)


class MeasurementViewSet(DetailSerializerMixin, ETAGMixin, CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    serializer_detail_class = MeasurementSerializer
    def retrieve(self, request, *args, **kwargs):
        return super(MeasurementViewSet, self).retrieve(request, *args, **kwargs)
    list_key_constructor_func = CookingNutritiousListKeyConstructor(memoize_for_request=True)
    @cache_control(private=True,max_age=31536000)
    @etag(list_key_constructor_func)
    @cache_response(31536000, key_func=list_key_constructor_func)
    def list(self, request, *args, **kwargs):
        return super(MeasurementViewSet, self).list(request, *args, **kwargs)


class MealCategoryViewSet(DetailSerializerMixin, ETAGMixin, CacheResponseMixin, viewsets.ReadOnlyModelViewSet):
    queryset = MealCategory.objects.all()
    serializer_class = MealCategorySerializer
    serializer_detail_class = MealCategorySerializer
    def retrieve(self, request, *args, **kwargs):
        return super(MealCategoryViewSet, self).retrieve(request, *args, **kwargs)
    list_key_constructor_func = CookingNutritiousListKeyConstructor(memoize_for_request=True)
    @cache_control(private=True,max_age=31536000)
    @etag(list_key_constructor_func)
    @cache_response(31536000, key_func=list_key_constructor_func)
    def list(self, request, *args, **kwargs):
        return super(MealCategoryViewSet, self).list(request, *args, **kwargs)
