from django.urls import path

from recipes import views

urlpatterns = [
    path("", views.RecipeList, name="index"),
    # path("signup/", views.SignUp.as_view(), name="recipes"),
    # path("signup/", views.SignUp.as_view(), name="shoplist"),
    path("new/", views.RecipeNew, name="recipe_new")
]