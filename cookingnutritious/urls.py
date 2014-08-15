from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User, Group
from django.contrib import admin
from rest_framework import routers 
from cookingnutritious import views

admin.autodiscover()

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'measurements', views.MeasurementViewSet)
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'recipies', views.RecipeViewSet)
router.register(r'recipeitems', views.RecipeItemViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    
    #url(r'^$', 'cookingnutritious.views.index', name='index'),
    url(r'^', include(router.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
