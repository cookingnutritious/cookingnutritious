from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from cookingnutritious import views
import autocomplete_light
# import every app/autocomplete_light_registry.py
autocomplete_light.autodiscover()
admin.autodiscover()

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register(r'mealcategories', views.MealCategoryViewSet)
router.register(r'mealingredients', views.MealIngredientViewSet)
router.register(r'mealitems', views.MealItemViewSet)
router.register(r'meals', views.MealViewSet)
router.register(r'recipes', views.RecipeViewSet)
router.register(r'recipeitems', views.RecipeItemViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'measurements', views.MeasurementViewSet)
router.register(r'photos', views.RecipePhotoViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'usda', views.FoodViewSet)
router.register(r'nutritionlogs', views.NutritionLogViewSet)
router.register(r'nutritionprofile', views.NutritionProfileViewSet)

template_name = {'template_name': 'rest_framework/login.html'}

urlpatterns = patterns('',
                       # url(r'^$', 'cookingnutritious.views.index', name='index'),
                       url(r'^', include(router.urls)),
                       url('', include('social.apps.django_app.urls', namespace='social')),
                       url('', include('django.contrib.auth.urls', namespace='auth')),
                       url(r'^login/$', 'django.contrib.auth.views.login', template_name, name='login'),
                       url(r"^payments/", include("payments.urls")),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^tinymce/', include('tinymce.urls')),
                       url(r'^autocomplete/', include('autocomplete_light.urls')),
                       url(r'^token/$', views.TokenRetrieve.as_view(), name='token'),
                       url(r'^nutrition/', views.NutritionList.as_view(), name='nutrition'),
                       url(r'^usda/search/(?P<long_description>[-_\w]+)/$',
                           views.FoodSearchViewSet.as_view({'get': 'list', }), name='usda-search'),
)
