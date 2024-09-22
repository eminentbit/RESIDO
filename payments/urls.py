from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.process_payment, name='process_payment'),
    path('pay', views.payments_view, name='pay'),
    path('process/monetbil_payment/', views.initiate_monetbil_payment, name='monetbil_payment'),
]