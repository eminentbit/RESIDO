from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', get_started, name='get_started'),
    path('home', home_view, name='dashboard_home'),
    path('my_listings', my_listings_view, name='dashboard_listing'),
    path('become_a_realtor', become_realtor, name='become_realtor'),
    path('profile', dashboard_profile_view, name='dashboard_profile'),
    path('chats', dashboard_chat, name='dashboard_chats'),
    path('settings', settings_view, name='dashboard_settings'),
    path('profile/edit', edit_profile, name='edit_profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
