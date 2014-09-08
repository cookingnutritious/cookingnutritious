from django.conf.urls import patterns, include, url
from usda import views

urlpatterns = patterns('usda.views',
    url(r'^$', views.FoodListView.as_view(), name='usda-food_list'),
    url(r'^(?P<pk>\d+)/$', views.FoodDetailView.as_view(), name='usda-food_detail'),
)
