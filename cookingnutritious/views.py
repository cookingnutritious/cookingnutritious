from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.formats import get_format
from django.views.decorators.cache import cache_control
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from food.models import (
    Measurement, 
    Ingredient,
    Recipe, 
    RecipeItem, 
    RecipePhoto, 
    MealCategory, 
    Tag, 
    Meal,
    MealItem,
    MealIngredient,
    compose_nutritional_information
)
from usda.models import Food 
from django.contrib.auth.models import User, Group
from cookingnutritious.serializers import (
    UserSerializer, 
    GroupSerializer, 
    MeasurementSerializer, 
    IngredientSerializer, 
    RecipeSerializer, 
    RecipeItemSerializer, 
    MealSerializer, 
    MealItemSerializer, 
    MealIngredientSerializer,
    RecipePhotoSerializer, 
    MealCategorySerializer, 
    TagSerializer, 
    FoodSerializer, 
    FoodDetailSerializer,
    TokenSerializer,
    NutritionSerializer
)
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
)
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
import urllib
import uuid
import warnings


class CookingNutritiousKeyConstructor(KeyConstructor):
    unique_view_id = bits.UniqueViewIdKeyBit()
    language = bits.LanguageKeyBit()
    format = bits.FormatKeyBit()
    callback = bits.QueryParamsKeyBit(
        ['callback', 'startdate', 'enddate']
    )


class CookingNutritiousRetrieveKeyConstructor(CookingNutritiousKeyConstructor):
    retrieve_sql_query = bits.RetrieveSqlQueryKeyBit()


class CookingNutritiousListKeyConstructor(CookingNutritiousKeyConstructor):
    list_sql_query = bits.ListSqlQueryKeyBit()


class RecipeListKeyConstructor(CookingNutritiousListKeyConstructor):
    user = bits.UserKeyBit()


class RecipeRetrieveKeyConstructor(CookingNutritiousRetrieveKeyConstructor):
    user = bits.UserKeyBit()


class MealListKeyConstructor(CookingNutritiousListKeyConstructor):
    user = bits.UserKeyBit()


class MealRetrieveKeyConstructor(CookingNutritiousRetrieveKeyConstructor):
    user = bits.UserKeyBit()


def index(request):
    context = RequestContext(request, {'request': request, 'user': request.user})
    return render_to_response('cookingnutritious/index.html', context_instance=context)


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

    def get_search_terms(self):
        search_list = self.request.GET.get('search', None)
        if search_list is not None:
            search_list = search_list.split(' ')
            return reduce(operator.and_, (Q(long_description__icontains=x) for x in search_list))
        else:
            return None

    def get_queryset(self, is_for_detail=False):
        terms = self.get_search_terms()
        limit = self.request.GET.get('limit', None)
        offset = self.request.GET.get('offset', None)
        if limit is not None:
            objects = Food.objects.filter(terms)[offset:limit]
        else:
            objects = Food.objects.all()[offset:limit]
        return objects
    retrieve_key_constructor_func = CookingNutritiousRetrieveKeyConstructor(memoize_for_request=True)

    @cache_control(private=True, max_age=31536000)
    @etag(retrieve_key_constructor_func)
    @cache_response(31536000, key_func=retrieve_key_constructor_func)
    def retrieve(self, request, *args, **kwargs):
        return super(FoodViewSet, self).retrieve(request, *args, **kwargs)
    list_key_constructor_func = CookingNutritiousListKeyConstructor(memoize_for_request=True)

    @cache_control(private=True, max_age=31536000)
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
        search_list = self.kwargs['long_description'].replace('_', ' ').replace('QQ', '.').replace('XX', '\'')\
            .replace('YY', '\"').replace('ZZ', '/').split(' ')
        return reduce(operator.and_, (Q(long_description__icontains=x) for x in search_list))

    def get_queryset(self, is_for_detail=False):
        terms = self.get_search_terms()
        return Food.objects.all().filter(terms)
    list_key_constructor_func = CookingNutritiousListKeyConstructor(memoize_for_request=True)

    @cache_control(private=True, max_age=31536000)
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

    @cache_control(private=True, max_age=31536000)
    @etag(retrieve_key_constructor_func)
    @cache_response(31536000, key_func=retrieve_key_constructor_func)
    def retrieve(self, request, *args, **kwargs):
        terms = self.get_search_terms()
        item = Food.objects.get(terms)
        serializer = FoodDetailSerializer(item, context={'request': request})
        return Response(serializer.data)


def recipe_list_cache_key(request):
    return '.'.join([
        'recipes',
        get_format(request)
    ])


def recipe_detail_cache_key(request, kwargs):
    return '.'.join([
        'recipes',
        kwargs['pk'],
        get_format(request)
    ])


class RecipeViewSet(DetailSerializerMixin, ETAGMixin, CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    serializer_detail_class = RecipeSerializer

    def get_queryset(self, is_for_detail=False):
        user = self.request.user
        recipes = Recipe.objects.filter(user=user)
        for recipe in recipes:
            recipe_items = RecipeItem.objects.filter(recipe=recipe)
            compose_nutritional_information(recipe, recipe_items)
        return recipes

    def get_object(self, queryset=None):
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
        compose_nutritional_information(obj, recipe_items)
        self.check_object_permissions(self.request, obj)
        return obj
    retrieve_key_constructor_func = RecipeRetrieveKeyConstructor(memoize_for_request=True)

    @cache_control(private=True, max_age=7200)
    @etag(retrieve_key_constructor_func)
    @cache_response(60 * 2, key_func=retrieve_key_constructor_func)
    def retrieve(self, request, *args, **kwargs):
        return super(RecipeViewSet, self).retrieve(request, *args, **kwargs)
    list_key_constructor_func = RecipeListKeyConstructor(memoize_for_request=True)

    @cache_control(private=True, max_age=7200)
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

    @cache_control(private=True, max_age=31536000)
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

    @cache_control(private=True, max_age=31536000)
    @etag(list_key_constructor_func)
    @cache_response(31536000, key_func=list_key_constructor_func)
    def list(self, request, *args, **kwargs):
        return super(MealCategoryViewSet, self).list(request, *args, **kwargs)


class TokenRetrieve(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    model = Token
    serializer_class = TokenSerializer

    def get_object(self, queryset=None):
        try:
            email = str(urllib.unquote(self.request.GET.get('email')).decode('UTF-8'))
            username = email.split("@")[0]
        except:
            raise Http404

        user = User.objects.filter(email=email).first()

        if user is None:
            if None != User.objects.filter(username=username).first():
                if len(username) == 30:
                    username = username[:16]
                username += str(uuid.uuid4().int)
                if len(username) > 30:
                    diff = 30 - len(username)
                    username = username[:diff]
            user = User.objects.create(username=username, email=email)
            user.save()

        return Token.objects.get(user=user)


class MealViewSet(DetailSerializerMixin, viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    serializer_detail_class = MealSerializer

    def get_queryset(self, is_for_detail=False):
        user = self.request.user
        meals = Meal.objects.filter(user=user)

        startdate = self.request.GET.get('startdate', None)
        enddate = self.request.GET.get('enddate', None)
        if startdate is not None:
            meals = meals.exclude(day__lt=startdate)
        if enddate is not None:
            meals = meals.exclude(day__gt=enddate)

        for meal in meals:
            meal_items = MealItem.objects.filter(meal=meal)
            compose_nutritional_information(meal, meal_items)
        return meals

    def get_object(self, queryset=None):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup = self.kwargs.get(lookup_url_kwarg, None)
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        obj_id = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)

        if lookup is not None:
            filter_kwargs = {self.lookup_field: lookup}
        elif obj_id is not None and self.lookup_field == 'obj_id':
            warnings.warn(
                PendingDeprecationWarning
            )
            filter_kwargs = {'obj_id': pk}
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
        compose_nutritional_information(obj, recipe_items)
        self.check_object_permissions(self.request, obj)
        return obj
    
    retrieve_key_constructor_func = MealRetrieveKeyConstructor(memoize_for_request=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            serializer.object.user = request.user
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        return super(MealViewSet, self).retrieve(request, *args, **kwargs)
    list_key_constructor_func = MealListKeyConstructor(memoize_for_request=True)

    def list(self, request, *args, **kwargs):
        return super(MealViewSet, self).list(request, *args, **kwargs)


class MealItemViewSet(viewsets.ModelViewSet):
    queryset = MealItem.objects.all()
    serializer_class = MealItemSerializer

    def get_queryset(self):
        user = self.request.user
        return MealItem.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            serializer.object.user = request.user
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MealIngredientViewSet(viewsets.ModelViewSet):
    queryset = MealIngredient.objects.all()
    serializer_class = MealIngredientSerializer

    def get_search_terms(self):
        exact = self.request.GET.get('exact', None)
        search_list = self.request.GET.get('search', None)

        if search_list is not None:
            if exact is not None:
                return Q(name=search_list)
            else:
                search_list = search_list.split(' ')
                return reduce(operator.and_, (Q(name__icontains=x) for x in search_list))
        else:
            return None

    def get_queryset(self, is_for_detail=False):
        user = self.request.user
        terms = self.get_search_terms()
        limit = self.request.GET.get('limit', None)
        offset = self.request.GET.get('offset', None)
        if limit is not None:
            objects = MealIngredient.objects.filter(terms, user=user)[offset:limit]
        else:
            objects = MealIngredient.objects.filter(user=user)[offset:limit]
        return objects

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            serializer.object.user = request.user
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)


class NutritionList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = NutritionSerializer

    def list(self, request):
        ingredient = Ingredient()
        return Response(Ingredient.get_field_names(ingredient))
