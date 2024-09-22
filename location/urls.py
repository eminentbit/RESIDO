from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('home', HomeView.as_view(), name='location-home'),
    path('geocoding/<int:pk>', GeoCodingView.as_view(), name='my-geocode'),
    path('', views.map_view, name='map')
]