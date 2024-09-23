from django.urls import path
from .views import RegisterView, RetrieveUserView, profile_view,signup_view


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('me', RetrieveUserView.as_view(), name='me'),
    path('profile', profile_view, name='profile'),
    path('signup', signup_view, name='signup'),
]
