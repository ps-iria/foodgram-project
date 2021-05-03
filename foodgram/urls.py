from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.db import router
from django.urls import path, include


router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('api/', include('api.urls')),
    # path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
