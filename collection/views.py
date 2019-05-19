from django.shortcuts import render
from django.urls import reverse_lazy #used to redirect to homepage when someone signs up sucessfully.
from django.views import generic
from django.contrib.auth.forms import UserCreationForm


def home(request):
	return render(request, 'collection/home.html')


class SignUp(generic.CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('home')
	template_name = 'registration/signup.html'
	