from django.urls import path

from recipes import views

urlpatterns = [
    path("", views.RecipeList, name="index"),
    # path("signup/", views.SignUp.as_view(), name="recipes"),
    # path("signup/", views.SignUp.as_view(), name="shoplist"),
    path("new/", views.RecipeNew, name="recipe_new"),
    path("recipe/<int:recipe_id>/", views.recipe, name="recipe"),
    path("recipe/<slug:recipe_slug>/", views.recipe_slug, name="recipe_slug"),
    path("recipe/<int:recipe_id>/edit/", views.recipe_edit, name="recipe_edit"),
    path("recipe/<slug:recipe_slug>/edit/", views.recipe_edit, name="recipe_edit"),
    path("recipe/<int:recipe_id>/delete/", views.recipe_delete, name="recipe_delete"),
    path('profile/<str:username>/', views.profile, name='profile'),
]