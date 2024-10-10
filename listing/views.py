from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Listing
from .serializers import ListingSerializer
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.contrib.auth.decorators import login_required
from .forms import ListingForm

class ManageListingView(APIView):
    def get(self, request, format=None):
        user = request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            return Response(
                {'error': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_realtor:
            return Response(
                {'error': 'User does not have necessary permissions for getting this listing data'},
                status=status.HTTP_403_FORBIDDEN
            )

        slug = request.query_params.get('slug')

        if not slug:
            listings = Listing.objects.filter(realtor=user.email).order_by('-date_created')
            serializer = ListingSerializer(listings, many=True)
            return Response({'listings': serializer.data}, status=status.HTTP_200_OK)

        try:
            listing = Listing.objects.get(realtor=user.email, slug=slug)
            serializer = ListingSerializer(listing)
            return Response({'listing': serializer.data}, status=status.HTTP_200_OK)
        except Listing.DoesNotExist:
            return Response({'error': 'Listing not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'Something went wrong when retrieving listing or listing detail'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        user = request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            return Response(
                {'error': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_realtor:
            return Response(
                {'error': 'User does not have necessary permissions for creating this listing data'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ListingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(realtor=user.email)
            return Response({'success': 'Listing created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug):
        user = request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            return Response(
                {'error': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_realtor:
            return Response(
                {'error': 'User does not have necessary permissions for updating this listing data'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            listing = Listing.objects.get(realtor=user.email, slug=slug)
        except Listing.DoesNotExist:
            return Response({'error': 'Listing does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ListingSerializer(listing, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'Listing updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        user = request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            return Response(
                {'error': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_realtor:
            return Response(
                {'error': 'User does not have necessary permissions for deleting this listing data'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            listing = Listing.objects.get(realtor=user.email, slug=slug)
            listing.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Listing.DoesNotExist:
            return Response({'error': 'Listing does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'Something went wrong when deleting listing'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListingDetailView(APIView):
    def get(self, request, format=None):
        slug = request.query_params.get('slug')

        if not slug:
            return Response({'error': 'Must provide slug'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            listing = Listing.objects.get(slug=slug, is_published=True)
            serializer = ListingSerializer(listing)
            return Response({'listing': serializer.data}, status=status.HTTP_200_OK)
        except Listing.DoesNotExist:
            return Response({'error': 'Published listing with this slug does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'error': 'Something went wrong when retrieving listing detail'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListingDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug = request.query_params.get('slug')

            if not slug:
                return Response(
                    {'error': 'Must provide slug'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not Listing.objects.filter(slug=slug, is_published=True).exists():
                return Response(
                    {'error': 'Published listing with this slug does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            listing = Listing.objects.get(slug=slug, is_published=True)
            listing = ListingSerializer(listing)

            return Response(
                {'listing': listing.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving listing detail'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# class ListingsView(APIView):
#     permission_classes = (permissions.AllowAny, )

#     def get(self, request, format=None):
#         try:
#             if not Listing.objects.filter(is_published=True).exists():
#                 return Response(
#                     {'error': 'No published listings in the database'},
#                     status=status.HTTP_404_NOT_FOUND
#                 )

#             listings = Listing.objects.order_by('-date_created').filter(is_published=True)
#             listings = ListingSerializer(listings, many=True)

#             return Response(
#                 {'listings': listings.data},
#                 status=status.HTTP_200_OK
#             )
#         except:
#             return Response(
#                 {'error': 'Something went wrong when retrieving listings'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

class SearchListingsView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        try:
            city = request.query_params.get('city')
            region = request.query_params.get('region')
            sqft = request.query_params.get('sqft')
            lot_size = request.query_params.get('lot_size')

            max_price = request.query_params.get('max_price')
            try:
                max_price = int(max_price)
            except:
                return Response(
                    {'error': 'Max price must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            bedrooms = request.query_params.get('bedrooms')
            try:
                bedrooms = int(bedrooms)
            except:
                return Response(
                    {'error': 'Bedrooms must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            parking_space = request.query_params.get('parking_space')
            try:
                parking_space = int(bedrooms)
            except:
                return Response(
                    {'error': 'parking_space must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            bathrooms = request.query_params.get('bathrooms')
            try:
                bathrooms = float(bathrooms)
            except:
                return Response(
                    {'error': 'Bathrooms must be a floating point value'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if bathrooms < 0 or bathrooms >= 10:
                bathrooms = 1.0

            bathrooms = round(bathrooms, 1)

            sale_type = request.query_params.get('sale_type')
            if sale_type == 'FOR_SALE':
                sale_type = 'For Sale'
            elif sale_type == 'GUEST_HOUSE':
                sale_type= 'guest_house'
            elif sale_type == ['HOTEL']:
                sale_type = 'hotel'
            else:
                sale_type = 'For Rent'

            home_type = request.query_params.get('home_type')
            if home_type == 'HOUSE':
                home_type = 'House'
            elif home_type == 'APARTMENT':
                home_type = 'APARTMENT'
            elif home_type == 'OFFICE_SPACE':
                home_type = 'office_space'
            else:
                home_type = 'Townhouse'

            search = request.query_params.get('search')
            if not search:
                return Response(
                    {'error': 'Must pass search criteria'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            vector = SearchVector('title', 'description')
            query = SearchQuery(search)

            if not Listing.objects.annotate(
                search=vector
            ).filter(
                search=query,
                city=city,
                region=region,
                price__lte=max_price,
                bedrooms__gte=bedrooms,
                parking_space=parking_space,
                bathrooms__gte=bathrooms,
                sale_type=sale_type,
                sqft=sqft,
                lot_size=lot_size,
                home_type=home_type,
                is_published=True
            ).exists():
                return Response(
                    {'error': 'No listings found with this criteria'},
                    status=status.HTTP_404_NOT_FOUND
                )

            listings = Listing.objects.annotate(
                search=vector
            ).filter(
                search=query,
                city=city,
                region=region,
                price__lte=max_price,
                bedrooms__gte=bedrooms,
                parking_space=parking_space,
                bathrooms__gte=bathrooms,
                sale_type=sale_type,
                sqft=sqft,
                lot_size=lot_size,
                home_type=home_type,
                is_published=True
            )
            listings = ListingSerializer(listings, many=True)

            return Response(
                {'listings': listings.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when searching for listings'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


def search_view(request):
    return render(request, 'listing/search.html')

def listings_view(request):
    try:
            if not Listing.objects.filter(is_published=True).exists():
                message = 'No published listings in the database'

            listings = Listing.objects.order_by('-date_created').filter(is_published=True)
            listings = ListingSerializer(listings, many=True)

            listings = listings.data
    except:
        message = 'Something went wrong when retrieving listings'
    total_listings = listings.count()
    active_listings = 0
    pending_listings = 0
    sold_listings = 0
    context = {
        'message': message,
        'listings': listings,
        'active_listings': active_listings,
        'pending_listings': pending_listings,
        'sold_listings': sold_listings,
        'total_listings': total_listings,
    }
    return render(request, 'listing/listings.html', context)

def listing_detail(request, id):
    listing = Listing.objects.filter(id=id)
    return render(request, 'listing/listing_detail.html', {'listing': listing})

@login_required
def add_listing_view(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect('all_listings')  # Redirect to the listings page
    else:
        form = ListingForm()
    
    return render(request, 'listing/add_listing.html', {'form': form})


def delete_listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    if request.method == 'POST':
        listing.delete()
        return redirect('/')
    return render(request,'listing/my_lising.html',{'listing':listing})

def modify_listing(request,id):
    listing = get_object_or_404(listing, id=id)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect ('listing_detail', id=listing.id)
    else:
        form = ListingForm(instance=listing)
        return render(request, 'modify_listing.html', {'form': form, 'listing': listing})



def contact(request):
    name = request.POST['name']
    email = request.POST['email']
    message = request.POST['message']