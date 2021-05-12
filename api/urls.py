from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter(trailing_slash=False)
router.register(r'ingredients',
                views.IngredientsViewSet,
                basename='ingredients')
router.register(r'follows',
                views.FollowsViewSet,
                basename='Follows')
router.register(r'favorites',
                views.FavoritesViewSet,
                basename='favorites')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/purchases/', views.add_purchase),
    path('v1/purchases/<int:id>', views.delete_purchase),
]
