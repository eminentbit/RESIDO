from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from listing.models import Listing

# Create your views here.

@login_required
def home_view(request):
    return render(request, 'dashboard/home.html')

@login_required
def my_listings_view(request):
    listings = Listing.objects.filter(realtor=request.user)
    total_listings = listings.count()
    active_listings = 0
    pending_listings = 0
    sold_listings = 0
    context = {
        'listings': listings,
        'active_listings': active_listings,
        'pending_listings': pending_listings,
        'sold_listings': sold_listings,
        'total_listings': total_listings,
    }
    return render(request, 'listing/my_listing.html', context)

@login_required
def dashboard_profile_view(request):
    return render(request, 'dashboard/my_profile.html')

@login_required
def settings_view(request):
    return render(request, 'dashboard/settings.html')

@login_required
def add_listing(request):
    pass    
