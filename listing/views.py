from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Listing
from .serializers import ListingSerializer
from django.contrib.postgres.search import SearchVector, SearchQuery

class ManageListingView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'User does not have necessary permissions for getting this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )

            slug = request.query_params.get('slug')

            if not slug:
                listing = Listing.objects.order_by('-date_created').filter(
                    realtor=user.email
                )
                listing = ListingSerializer(listing, many=True)
                
                return Response(
                    {'listings': listing.data},
                    status=status.HTTP_200_OK
                )

            if not Listing.objects.filter(
                realtor=user.email,
                slug=slug
            ).exists():
                return Response(
                    {'error': 'Listing not found'},
                    status=status.HTTP_404_NOT_FOUND
                )

            listing = Listing.objects.get(realtor=user.email, slug=slug)
            listing = ListingSerializer(listing)

            return Response(
                {'listing': listing.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving listing or listing detail'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve_values(self, data):
        title = data['title']
        slug = data['slug']
        address = data['address']
        city = data['city']
        region = data['region']
        zipcode = data['zipcode']
        description = data['description']
        sqft = data['sqft']
        lot_size = data[lot_size]

        price = data['price']
        try:
            price = int(price)
        except:
            return -1

        bedrooms = data['bedrooms']
        try:
            bedrooms = int(bedrooms)
        except:
            return -2
        
        parking_space = data['parking']
        try:
            parking = int(parking_space)
        except:
            return -3

        bathrooms = data['bathrooms']
        try:
            bathrooms = float(bathrooms)
        except:
            return -4

        if bathrooms <= 0 or bathrooms >= 10:
            bathrooms = 1.0

        bathrooms = round(bathrooms, 1)

        sale_type = data['sale_type']
        
        if sale_type == 'FOR_RENT':
            sale_type = 'For Rent'
        elif sale_type == 'GUEST_HOUSE':
            sale_type= 'guest_house'
        elif sale_type == ['HOTEL']:
            sale_type = 'hotel'
        else:
            sale_type = 'For Sale'

        home_type = data['home_type']

        if home_type == 'APARTMENT':
            home_type = 'apartment'
        elif home_type == 'TOWNHOUSE':
            home_type = 'Townhouse'
        elif home_type == 'OFFICE_SPACE':
            home_type = 'office_space'
        else:
            home_type = 'House'
        
        main_photo = data['main_photo']
        photo_1 = data['photo_1']
        photo_2 = data['photo_2']
        photo_3 = data['photo_3']
        photo_4 = data['photo_4']
        photo_5 = data['photo_5']
        photo_6 = data['photo_6']
        photo_7 = data['photo_7']
        photo_8 = data['photo_8']
        photo_9 = data['photo_9']
        photo_10 = data['photo_10']
        video_files = data['video_files']
        is_published = data['is_published']

        if is_published == 'True':
            is_published = True
        else:
            is_published = False

        data = {
            'title': title,
            'slug': slug,
            'address': address,
            'city': city,
            'region': region,
            'zipcode': zipcode,
            'description': description,
            'price': price,
            'bedrooms': bedrooms,
            'parking_space':parking_space,
            'bathrooms': bathrooms,
            'sqft' : sqft,
            'lot_size' : lot_size,
            'sale_type': sale_type,
            'home_type': home_type,
            'main_photo': main_photo,
            'photo_1': photo_1,
            'photo_2': photo_2,
            'photo_3': photo_3,
            'photo_4': photo_4,
            'photo_5': photo_5,
            'photo_6': photo_6,
            'photo_7':photo_7,
            'photo_8':photo_8,
            'photo_9':photo_9,
            'photo_10':photo_10,
            'video_files':video_files,
            'is_published': is_published
        }

        return data

    def post(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'User does not have necessary permissions for creating this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data

            data = self.retrieve_values(data)

            if data == -1:
                return Response(
                    {'error': 'Price must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif data == -2:
                return Response(
                    {'error': 'Bedrooms must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif data == -3:
                return Response(
                    {'error': 'Bathrooms must be a floating point value'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            title = data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            region = data['region']
            zipcode = data['zipcode']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            sqft = data['sqft']
            lot_size = data['lot_size']
            parking_space = data['parking_space']
            bathrooms = data['bathrooms']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            photo_4 = data['photo_4']
            photo_5 = data['photo_5']
            photo_6 = data['photo_6']
            photo_7 = data['photo_7']
            photo_8 = data['photo_8']
            photo_9 = data['photo_9']
            photo_10 = data['photo_10']
            video_files = data['video_files']
            is_published = data['is_published']

            if Listing.objects.filter(slug=slug).exists():
                return Response(
                    {'error': 'Listing with this slug already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            Listing.objects.create(
                realtor=user.email,
                title=title,
                slug=slug,
                address=address,
                city=city,
                region=region,
                zipcode=zipcode,
                description=description,
                price=price,
                bedrooms=bedrooms,
                parking_space=parking_space,
                bathrooms=bathrooms,
                sqft=sqft,
                lot_size=lot_size,
                sale_type=sale_type,
                home_type=home_type,
                main_photo=main_photo,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                photo_4=photo_4,
                photo_5=photo_5,
                photo_6=photo_6,
                photo_7=photo_7,
                photo_8=photo_8,
                photo_9=photo_9,
                photo_10=photo_10,
                video_files=video_files,
                is_published=is_published
            )

            return Response(
                {'success': 'Listing created successfully'},
                status=status.HTTP_201_CREATED
            )
        except:
            return Response(
                {'error': 'Something went wrong when creating listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'User does not have necessary permissions for updating this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data

            data = self.retrieve_values(data)

            if data == -1:
                return Response(
                    {'error': 'Price must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif data == -2:
                return Response(
                    {'error': 'Bedrooms must be an integer'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif data == -3:
                return Response(
                    {'error': 'Bathrooms must be a floating point value'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            title = data['title']
            slug = data['slug']
            address = data['address']
            city = data['city']
            region = data['region']
            zipcode = data['zipcode']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            parking_space = data['parking_space']
            bathrooms = data['bathrooms']
            sqft = data['sqft']
            lot_size =['lot_size']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            photo_4 = data['photo_4']
            photo_5 = data['photo_5']
            photo_6 = data['photo_6']
            photo_7 = data['photo_7']
            photo_8 = data['photo_8']
            photo_9 = data['photo_9']
            photo_10 = data['photo_10']
            video_files= data['video_files']
            is_published = data['is_published']

            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            Listing.objects.filter(realtor=user.email, slug=slug).update(
                title=title,
                slug=slug,
                address=address,
                city=city,
                region = region,
                zipcode=zipcode,
                description=description,
                price=price,
                bedrooms=bedrooms,
                sqft=sqft,
                lot_size=lot_size,
                parking_space=parking_space,
                bathrooms=bathrooms,
                sale_type=sale_type,
                home_type=home_type,
                main_photo=main_photo,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                photo_4=photo_4,
                photo_5=photo_5,
                photo_6=photo_6,
                photo_7=photo_7,
                photo_8=photo_8,
                photo_9=photo_9,
                photo_10=photo_10,
                video_files=video_files,
                is_published=is_published
            )

            return Response(
                {'success': 'Listing updated successfully'},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when updating listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'User does not have necessary permissions for updating this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data

            slug = data['slug']

            is_published = data['is_published']
            if is_published == 'True':
                is_published = True
            else:
                is_published = False

            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            Listing.objects.filter(realtor=user.email, slug=slug).update(
                is_published=is_published
            )

            return Response(
                {'success': 'Listing publish status updated successfully'},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when updating listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        try:
            user = request.user

            if not user.is_realtor:
                return Response(
                    {'error': 'User does not have necessary permissions for deleting this listing data'},
                    status=status.HTTP_403_FORBIDDEN
                )

            data = request.data

            try:
                slug = data['slug']
            except:
                return Response(
                    {'error': 'Slug was not provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    {'error': 'Listing you are trying to delete does not exist'},
                    status=status.HTTP_404_NOT_FOUND
                )

            Listing.objects.filter(realtor=user.email, slug=slug).delete()

            if not Listing.objects.filter(realtor=user.email, slug=slug).exists():
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
            else:
                return Response(
                    {'error': 'Failed to delete listing'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'Something went wrong when deleting listing'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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

class ListingsView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        try:
            if not Listing.objects.filter(is_published=True).exists():
                return Response(
                    {'error': 'No published listings in the database'},
                    status=status.HTTP_404_NOT_FOUND
                )

            listings = Listing.objects.order_by('-date_created').filter(is_published=True)
            listings = ListingSerializer(listings, many=True)

            return Response(
                {'listings': listings.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving listings'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
    listings = Listing.objects.all()
    return render(request, 'listing/listing1.html', {'listings': listings})

def contact(request):
    pass