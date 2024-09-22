from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),
    path('auth/user/', include('user.urls')),
    path('api/listing/', include('listing.urls')),
    #path('', include('project_content.urls')),
    path('payments/', include('payments.urls')),
    path('admin/', admin.site.urls),
    path('location/', include('location.urls')),
]