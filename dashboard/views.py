from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse_lazy

from listing.models import Listing
User = get_user_model()

# Create your views here.

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
    if request.user.is_realtor:
        return render(request, 'dashboard/my_profile.html', {'profile_pic': request.user.profile.image.url})
    else:
        return redirect(reverse_lazy('become_realtor'))

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Update profile picture if submitted
        if 'profile_picture' in request.FILES:
            request.user.profile.image = request.FILES['profile_picture']
            request.user.profile.save()

        # Update other profile details
        if 'first_name' in request.POST and 'last_name' in request.POST:
            user = request.user
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.profile.phone = request.POST.get('phone', '')  # Default to empty string if phone is not provided
            user.save()
            user.profile.save()

        messages.success(request, 'Your profile has been updated!')
        return redirect('dashboard_profile')  # Redirect after saving changes
    else:
        return render(request, 'dashboard/my_profile.html')

@login_required
def messages_view(request):
    return render(request, 'dashboard/messages.html')

@login_required
def settings_view(request):
    return render(request, 'dashboard/settings.html')

@login_required
def add_listing(request):
    pass    

def get_started(request):
    if request.user.is_authenticated:
        if request.user.is_realtor:
            return redirect('dashboard_home')
        else:
            return render(request, 'dashboard/index.html')
    else:
        return redirect('login')
        


@login_required
def become_realtor(request):
    if request.method == 'POST':
        realtor_status = request.POST.get('realtor', 'False') == 'True'
        request.user.is_realtor = realtor_status
        request.user.save()  # Save the changes to the user model
        if request.user.is_realtor:
            return redirect(reverse_lazy('dashboard_home'))
        else:
            return redirect(reverse_lazy('get_started'))
    
    return render(request, 'dashboard/become_realtor.html')