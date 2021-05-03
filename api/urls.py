from django.db import router
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import registration, get_token

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
    path('v1/auth/email/', registration),
    path('v1/auth/token/', get_token),
]