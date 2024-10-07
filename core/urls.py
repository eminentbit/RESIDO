from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.conf.urls.static import static

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),
    path('auth/user/', include('user.urls')),
    path('listing/', include('listing.urls')),
    #path('', include('project_content.urls')),
    path('payments/', include('payments.urls')),
    path('admin/', admin.site.urls),
    path('location/', include('location.urls')),
    path('', include('user.urls')),
    path('auth/', include('authentication.urls')),
    path('chat/', include('chat.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)