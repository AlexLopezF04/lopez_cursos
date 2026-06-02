# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from store.views import RegistroView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Auth JWT
    path('api/auth/registro/', RegistroView.as_view(),          name='auth-registro'),
    path('api/auth/login/',    TokenObtainPairView.as_view(),   name='auth-login'),
    path('api/auth/refresh/',  TokenRefreshView.as_view(),      name='auth-refresh'),
    path('api/auth/logout/',   TokenBlacklistView.as_view(),    name='auth-logout'),

    # App
    path('api/', include('store.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)