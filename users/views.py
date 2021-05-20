from django.contrib.auth import get_user_model
from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy

from .forms import CreationForm

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    template_name = '../templates/signup.html'
    success_url = reverse_lazy("index")  # done
