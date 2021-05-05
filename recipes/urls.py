from django.urls import path

from users import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="recipes"),
    path("signup/", views.SignUp.as_view(), name="shoplist"),
]