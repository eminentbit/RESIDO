from django.urls import path
from .views import RegisterView, RetrieveUserView, profile_view,signup_view, SignInView, signout, home_view


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('me', RetrieveUserView.as_view(), name='me'),
    path('profile', profile_view, name='profile'),
    path('signup', signup_view, name='signup'),
    path('login', SignInView.as_view(), name='login'),
    path('signout', signout, name='signout'),
    path('', home_view,name='home')
]
