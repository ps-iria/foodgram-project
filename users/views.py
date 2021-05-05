from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse_lazy
from django.views.generic import CreateView
from .forms import CreationForm

User = get_user_model()


class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy("index")  # done
