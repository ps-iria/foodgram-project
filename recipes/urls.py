from django.urls import path

from recipes import views

urlpatterns = [
    path("", views.recipe_list, name="index"),
    path("new/", views.recipe_new, name="recipe_new"),
    path("recipe/<int:recipe_id>/", views.recipe, name="recipe"),
    path("recipe/<slug:recipe_slug>/", views.recipe_slug, name="recipe_slug"),
    path("recipe/<int:recipe_id>/edit/", views.recipe_edit, name="recipe_edit"),
    path("recipe/<slug:recipe_slug>/edit/", views.recipe_edit, name="recipe_edit"),
    path("recipe/<int:recipe_id>/delete/", views.recipe_delete, name="recipe_delete"),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('follow/', views.follow_list, name='follow'),
    path('favorite/', views.favorite_list, name='favorite'),
    path('purchase/', views.purchase, name='purchase'),
    path('purchase/delete/<int:recipe_id>/', views.delete_purchase, name='delete_purchase'),
    path('purchase/download/', views.download_purchase, name='download_purchase'),
]