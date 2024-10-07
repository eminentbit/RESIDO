from django.urls import path
from .views import *


urlpatterns = [
    path('api/manage', ManageListingView.as_view()),
    path('api/detail', ListingDetailView.as_view()),
    # path('api/get-listings', ListingsView.as_view()),
    path('api/searching', SearchListingsView.as_view()),
    path('search', search_view, name='search'),
    path('', listings_view, name='all_listings'),
    path('contact', contact, name='contact'),
    path('<int:id>', listing_detail, name='listing'),
]
