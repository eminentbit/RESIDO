from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home_view(request):
    return render(request, 'dashboard/home.html')

@login_required
def my_listings_view(request):
    return render(request, 'listing/my_listing.html')

@login_required
def dashboard_profile_view(request):
    return render(request, 'dashboard/my_profile.html')

@login_required
def settings_view(request):
    return render(request, 'dashboard/settings.html')

@login_required
def add_listing(request):
    pass    
