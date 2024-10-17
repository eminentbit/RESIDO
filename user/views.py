from django.conf import settings
from django.contrib.auth import get_user_model, logout, login, authenticate, views
from django.http import JsonResponse
from django.shortcuts import redirect, render

from django.urls import reverse, reverse_lazy
from allauth.account.views import LoginView

from listing.models import Listing

from user.forms import AuthForm, UserForm, UserProfileForm
from django.views.generic.edit import FormView
from user.mixin import AjaxFormMixin, FormErrors, reCAPTCHAValidation
from user.models import UserProfile
User = get_user_model()
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# class RegisterView(APIView, AjaxFormMixin):
#     permission_classes = (permissions.AllowAny, )


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['recaptcha_site_key'] = settings.RECAPTCHA_PUBLIC_KEY
#         return context
    
#     # def get(self, request, *args, **kwargs):
#     #     # Context data for the template (if needed)
#     #     context = context = {
#     #         'recaptcha_site_key': settings.RECAPTCHA_PUBLIC_KEY
#     #     }
#     #     return render(request, 'user/signup.html', context)

#     def form_valid(self, form):
#         # Call the parent class's form_valid method
#         response = super().form_valid(form)

#         # Check if the request is an AJAX request
#         if self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#             token = form.cleaned_data.get('token')
#             captcha = reCAPTCHAValidation(token)
            
#             if captcha.get('SUCCESS'):
#                 try:
#                     obj = form.save()
                    
#                     # Assuming userprofile should be created or available
#                     up = getattr(obj, 'userprofile', None)
#                     if up is None:
#                         up = UserProfile.objects.create(user=obj)  # Create user profile if not existing
                    
#                     up.captcha_score = float(captcha.get('score', 0))
#                     up.save()

#                     # Log the user in
#                     login(self.request, obj, backend='django.contrib.auth.backends.ModelBackend')

#                     return JsonResponse({
#                         'result': 'Success',
#                         'message': 'Thank you for signing up'
#                     }, status=201)

#                 except Exception as e:
#                     return JsonResponse({
#                         'result': 'Failure',
#                         'message': str(e)
#                     }, status=500)
#             else:
#                 return JsonResponse({
#                     'result': 'Failure',
#                     'message': 'Captcha verification failed'
#                 }, status=400)

#         return response  # Return the original response if not an AJAX request


#     def post(self, request):
#         try:
#             data = request.data

#             first_name = data.get('first_name')
#             last_name = data.get('last_name')
#             email = data.get('email').lower()
#             password = data.get('password')
#             re_password = data.get('re_password')
#             is_realtor = data.get('is_realtor', '').lower() == 'true'

#             # Password validation
#             if password != re_password:
#                 return Response(
#                     {'error': 'Passwords do not match'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             if len(password) < 8:
#                 return Response(
#                     {'error': 'Password must be at least 8 characters long'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             # Check if the email is already registered
#             if User.objects.filter(email=email).exists():
#                 return Response(
#                     {'error': 'A user with this email already exists'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )

#             # Create and save the user
#             user = User.objects.create_user(
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email,
#                 password=password
#             )
#             user.is_realtor = is_realtor
#             user.save()

#             return Response(
#                 {'success': 'User created successfully'},
#                 status=status.HTTP_201_CREATED
#             )

#         except Exception as e:
#             return Response(
#                 {'error': str(e)},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
        
class RegisterView(FormView):
    template_name = 'user/signup.html'
    form_class = UserForm
    success_url = reverse_lazy('dashboard_home')

    def form_valid(self, form):
        # Get the reCAPTCHA token from the form
        captcha_token = self.request.POST.get('captcha_token')

        # Validate the reCAPTCHA token
        recaptcha_result = reCAPTCHAValidation(captcha_token)

        if recaptcha_result.get('success'):
            try:
                user = form.save()  # Save the user if reCAPTCHA is valid
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(self.request, user)
                return super().form_valid(form)
            except Exception as e:
                form.add_error(None, str(e))  # Attach any other exception to the form
                return self.form_invalid(form)
        else:
            # If reCAPTCHA validation fails, add an error
            form.add_error(None, "Invalid reCAPTCHA. Please try again.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Handles case where form is invalid and re-renders with errors
        print(form.errors)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add reCAPTCHA site key to context for use in the template
        context['recaptcha_site_key'] = settings.RECAPTCHA_PUBLIC_KEY
        return context
    

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
        
def about_view(request):
    return render(request, 'About_us.html')


@login_required        
def profile_view(request):
    '''
    Function view to allow users to update their profile
    '''
    user = request.user
    up = request.user.profile  

    if not up:
        return JsonResponse({'result': 'error', 'message': 'Profile not found'}, status=404)

    form = UserProfileForm(instance=up)
    result = 'error'  # Default to error

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = UserProfileForm(data=request.POST, instance=up)
        if form.is_valid():
            obj = form.save()
            obj.has_profile = True
            obj.save()
            result = 'success'
            message = 'Your Profile has been updated'
        else:
            message = FormErrors(form)
        data = {'result': result, 'message': message, 'redirect_url': reverse_lazy('home')}
        return render(request, 'profile_updated.html', data)
    
    else:
        context = {
            'form': form,
            'google_api_key': settings.GOOGLE_API_KEY,
            'base_country': settings.BASE_COUNTRY
        }
        return render(request, 'user/profile.html', context)
    

class SignInView(LoginView):
    template_name = 'user/sign_in.html'

    def get_success_url(self):
        return '/auth/signin' 
    
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
                # request.session.set_expiry(60 * 60 * 24 * 365 * 5)
                return redirect('dashboard_home')  # Redirect to a success page or home page
            else:
                message = 'Invalid credentials'
                return render(request, template_name='user/signup.html', context={'error': message})
        else:
            message = form.errors
            return render(request, template_name='user/signup.html', context={'error': message})
        

def sign_in(request):
    if request.method == 'POST':
        form = AuthForm(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')  # Username field is used for email in AuthForm
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard_home')  # Redirect to a homepage or dashboard
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Invalid reCAPTCHA. Please try again.")
    else:
        form = AuthForm()

    return render(request, 'user/sign_in.html', {'form': form})


def home_view(request):
    listings = Listing.objects.all()
    return render(request, 'home.html', {'listings': listings})

@login_required
def password_change(request):
    current_user = request.user
    if request.method == 'POST':
        current_user.set_password(request.POST['new_password'])
        current_user.save()
        change_done = "Password successfully changed"
        context = {'current_user': current_user, 'change_done': change_done}
        return render(request, 'user/change_password.html', context)

    context = {'current_user': current_user }
    return render(request, 'user/change_password.html', context)


def get_all_realtors(request):
    realtors = User.objects.filter(is_realtor=True) 
    return render(request, 'realtors.html', {'realtors': realtors})

  
def signout(request):
    '''
    Basic View for the user to Sign Out
    '''
    logout(request)
    return redirect(reverse('login'))

def browse_homes(request):
    return render('browse_homes.html')


def all_homes_view(request):
    return render(request, 'all_homes.html')


# SALE
def homes_for_sale(request):
    return render(request, 'sale/homes.html')

def construction_for_sale(request):
    return render(request, 'sale/new_construction.html')

def appartments_for_sale(request):
    return render(request, 'sale/appartments.html')

def townhouses_for_sale(request):
    return render(request, 'sale/townhouses.html')

def construction_for_sale(request):
    return render(request, 'sale/new_construction.html')

def office_for_sale(request):
    return render(request, 'sale/office_spaces.html')

# RENT
def homes_for_rent(request):
    return render(request, 'rent/homes.html')

def construction_for_rent(request):
    return render(request, 'rent/new_construction.html')

def appartments_for_rent(request):
    return render(request, 'rent/appartments.html')

def townhouses_for_rent(request):
    return render(request, 'rent/townhouses.html')

def office_for_rent(request):
    return render(request, 'rent/office_spaces.html')
