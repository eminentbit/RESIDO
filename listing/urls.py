from django.urls import path
from .views import *


urlpatterns = [
    path('manage', ManageListingView.as_view()),
    path('detail', ListingDetailView.as_view()),
    path('get-listings', ListingsView.as_view()),
    path('searching', SearchListingsView.as_view()),
    path('search', search_view, name='search'),
    path('', listings_view, name='listings'),
    path('contact', contact, name='contact'),
]
