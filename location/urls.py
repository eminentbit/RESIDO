from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # path('home', HomeView.as_view(), name='location-home')
    path('', views.map_view, name='map_test'),
    # path('route', views.route, name='route'),
    # path('map', views.map, name='map'),
]