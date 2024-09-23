from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.process_payment, name='process_payment'),
    path('pay', views.payments_view, name='pay'),
    path('process/monetbil_payment/', views.initiate_monetbil_payment, name='monetbil_payment'),
    path('monetbil/payment/', views.monetbil_payment, name='monetbil_payment'),
    path('error', views.payment_error, name='payment_error'),
    path('success', views.payment_success, name='payment_success')
]