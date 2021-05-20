from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views
from django.urls import path, include


urlpatterns = [
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
    path('', include('recipes.urls')),
    path('about/', include('django.contrib.flatpages.urls')),
]

urlpatterns += [
    path('about-author/', views.flatpage, {'url': '/about-author/'},
         name='author'),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='spec'),
]

handler404 = 'foodgram.views.page_not_found'
handler500 = 'foodgram.views.server_error'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
