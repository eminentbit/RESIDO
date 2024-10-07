from django.urls import path
from .views import *


urlpatterns = [
    path('', home_view, name='dashboard_home'),
    path('my_listings', my_listings_view, name='my_listings'),
    path('profile', dashboard_profile_view, name='dashboard_profile'),
]