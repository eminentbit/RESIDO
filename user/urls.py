from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Not directly related
    path('homes_rent', homes_for_sale, name='homes_rent'),
    path('realtors', get_all_realtors, name='realtors'),

    # Directly related
    path('register', RegisterView.as_view(), name='register'),
    path('me', RetrieveUserView.as_view(), name='me'),
    path('profile', profile_view, name='profile'),
    path('login', SignInView.as_view(), name='login'),
    path('signout', signout, name='signout'),
    path('', home_view, name='home'),
    path('change_pass', password_change, name='change_password'),
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='user/password_reset_form.html'), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), 
         name='password_reset_complete'),
]
