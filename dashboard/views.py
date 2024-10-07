from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home_view(request):
    return render(request, 'dashboard/home.html')

def my_listings_view(request):
    pass
    return render(request, 'dashboard/my_listing.html')

def dashboard_profile_view(request):
    return render(request, 'dashboard/my_profile.html')
