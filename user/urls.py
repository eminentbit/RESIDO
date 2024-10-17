from django.urls import path # type: ignore
from .views import *
from django.contrib.auth import views as auth_views # type: ignore


urlpatterns = [
    # Not directly related
    path('realtors', get_all_realtors, name='realtors'),
    path('about_us', about_view, name='about_us'),
    path('all_homes', all_homes_view, name='all_homes'),

     # RENT 
    path('rent/homes', homes_for_rent, name='homes_rent'),
    path('rent/townhouses', townhouses_for_rent, name='townhouses_rent'),
    path('rent/constructions', construction_for_rent, name='construction_rent'),
    path('rent/appartments', appartments_for_rent, name='appartments_rent'),
    path('rent/office_spaces', office_for_rent, name='officespaces_rent'),

     # SALE
    path('sell/homes', homes_for_sale, name='homes_sell'),
    path('sell/townhouses', townhouses_for_sale, name='townhouses_sell'),
    path('sell/constructions', construction_for_sale, name='construction_sell'),
    path('sell/appartments', appartments_for_sale, name='appartments_sell'),
    path('sell/office_spaces', office_for_sale, name='officespace_sell'),

    # Directly related
    path('accounts/profile/', profile_view, name='profile'),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('me', RetrieveUserView.as_view(), name='me'),
    path('profile', profile_view, name='profile'),
    path('auth/signin', sign_in, name='login'),
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
