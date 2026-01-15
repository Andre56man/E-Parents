"""URL configuration for eparent project."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('accounts.urls')),
    path('notifications/', include('notifications.urls')),
    path('messaging/', include('messaging.urls')),

    # API principale (pour React Native)
    path('api/', include('core.api_urls', namespace='core_api')),

    # API Notifications & Messagerie
    path('api/notifications/', include('notifications.api_urls', namespace='notifications_api')),
    path('api/messaging/', include('messaging.api_urls', namespace='messaging_api')),

    # API Auth JWT pour lapp React Native
    path('api/auth/jwt/create/', TokenObtainPairView.as_view(), name='jwt_create'),
    path('api/auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),

    # API Auth JWT pour lapp React Native
    path('api/auth/', include('djoser.urls')),         # <--- AJOUTEZ CECI (pour /me/)
    path('api/auth/', include('djoser.urls.jwt')),
]

# Servir les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

