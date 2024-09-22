from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from .models import *
from django.conf import settings

# Create your views here.
class HomeView(ListView):
    template_name = 'location/home.html'
    context_object_name = 'mydata'
    model = Locations
    success_url = '/'

class GeoCodingView(View):
    template_name = 'location/geocoding.html'

    def get(self, request, pk):
        location = Locations.objects.get(pk=pk)

        context = {
            'location': location
        }

        return render(request, self.template_name, context)
    

def map_view(request):
    return render(request, 'location/map.html', {'google_maps_api_key': settings.GOOGLE_API_KEY})