from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model, logout, login, authenticate
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm

from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import FormView

from listing.models import Listing

from user.forms import AuthForm, UserProfileForm, UserCreationForm
from user.mixin import AjaxFormMixin, FormErrors, reCAPTCHAValidation
from user.models import UserAccount, UserProfile
User = get_user_model()
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth.decorators import login_required


class RegisterView(APIView, AjaxFormMixin):
    permission_classes = (permissions.AllowAny, )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recaptcha_site_key'] = settings.RECAPTCHA_PUBLIC_KEY
        return context
    
    # def get(self, request, *args, **kwargs):
    #     # Context data for the template (if needed)
    #     context = context = {
    #         'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY
    #     }
    #     return render(request, 'user/signup.html', context)

    def form_valid(self, form):
        # Call the parent class's form_valid method
        response = super().form_valid(form)

        # Check if the request is an AJAX request
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            token = form.cleaned_data.get('token')
            captcha = reCAPTCHAValidation(token)
            
            if captcha.get('SUCCESS'):
                try:
                    obj = form.save()
                    
                    # Assuming userprofile should be created or available
                    up = getattr(obj, 'userprofile', None)
                    if up is None:
                        up = UserProfile.objects.create(user=obj)  # Create user profile if not existing
                    
                    up.captcha_score = float(captcha.get('score', 0))
                    up.save()

                    # Log the user in
                    login(self.request, obj, backend='django.contrib.auth.backends.ModelBackend')

                    return JsonResponse({
                        'result': 'Success',
                        'message': 'Thank you for signing up'
                    }, status=201)

                except Exception as e:
                    return JsonResponse({
                        'result': 'Failure',
                        'message': str(e)
                    }, status=500)
            else:
                return JsonResponse({
                    'result': 'Failure',
                    'message': 'Captcha verification failed'
                }, status=400)

        return response  # Return the original response if not an AJAX request


    def post(self, request):
        try:
            data = request.data

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            email = data.get('email').lower()
            password = data.get('password')
            re_password = data.get('re_password')
            is_realtor = data.get('is_realtor', '').lower() == 'true'

            # Password validation
            if password != re_password:
                return Response(
                    {'error': 'Passwords do not match'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if len(password) < 8:
                return Response(
                    {'error': 'Password must be at least 8 characters long'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if the email is already registered
            if User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'A user with this email already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create and save the user
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            user.is_realtor = is_realtor
            user.save()

            return Response(
                {'success': 'User created successfully'},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RetrieveUserView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Something went wrong when retrieving user details'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
def profile_view(request):
    '''
    Function view to allow users to update their profile
    '''
    user = request.user
    up = user.profile

    form = UserProfileForm(instance = up)

    if request.is_ajax():
        form = UserProfileForm(data=request.POST, instance=up)
        if form.is_valid():
            obj = form.save()
            obj.has_profile = True
            obj.save()
            result = 'Success'
            message = 'Your Profile has been updated'
        else:
            message = FormErrors(form)
        data = {'result': result, 'message': message}
        return JsonResponse(data)
    
    else:
        context = {'form': form}
        context['google_api_key'] = settings.GOOGLE_API_KEY
        context['base_country'] = settings.BASE_COUNTRY

        return render(request, 'user/profile.html', context)
    
def signup_view(request):
    return render(request, 'user/signup.html')

class SignInView(View):
    template_name = 'user/sign_in.html'
    
    def get(self, request):
        form = AuthForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = AuthForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                message = 'You are now logged in now'
                return redirect(reverse_lazy('map_test'))
            else:
                message = 'Invalid credentials'
                return render(request, template_name='user/signup.html', context={'error': message})
        else:
            message = form.errors
            return render(request, template_name='user/signup.html', context={'error': message})


def home_view(request):
    listings = Listing.objects.all()
    return render(request, 'home.html', {'listings': listings})
        

def signout(request):
    '''
    Basic View for the user to Sign Out
    '''
    logout(request)
    return redirect(reverse('sign-in'))