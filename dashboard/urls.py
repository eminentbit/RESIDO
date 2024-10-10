from django.urls import path
from .views import *


urlpatterns = [
    path('', home_view, name='dashboard_home'),
    path('my_listings', my_listings_view, name='dashboard_listing'),
    path('profile', dashboard_profile_view, name='dashboard_profile'),
    path('settings', settings_view, name='dashboard_settings')
]