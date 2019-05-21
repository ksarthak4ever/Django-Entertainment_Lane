from django.shortcuts import render, redirect
from django.urls import reverse_lazy #used to redirect to homepage when someone signs up sucessfully.
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login 
from .models import Collection,Video
from .forms import VideoForm, SearchForm


def home(request):
	return render(request, 'collection/home.html')

def dashboard(request):
	return render(request, 'collection/dashboard.html')

def add_video(request, pk):
	form = VideoForm()
	search_form = SearchForm()

	if request.method == 'POST':
		filled_form = VideoForm(request.POST)
		if filled_form.is_valid():
			video = Video()
			video.url = filled_form.cleaned_data['url']
			video.title = filled_form.cleaned_data['title']
			video.youtube_id = filled_form.cleaned_data['youtube_id']
			video.collection = Collection.objects.get(pk=pk)
			video.save()

	return render(request, 'collection/add_video.html', {'form':form, 'search_form':search_form})


class SignUp(generic.CreateView):
	form_class = UserCreationForm
	success_url = reverse_lazy('home')
	template_name = 'registration/signup.html'

	def form_valid(self, form): #to login user as soon as he signsup
		view = super(SignUp, self).form_valid(form)
		username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
		user = authenticate(username=username, password=password)
		login(self.request, user)
		return view
	

class create_collection(generic.CreateView):
	model = Collection
	fields = ['title']
	template_name = 'collection/create_collection.html'
	success_url = reverse_lazy('home')

	def form_valid(self, form):
		form.instance.user = self.request.user
		super(create_collection, self).form_valid(form)
		return redirect('home')


class detail_collection(generic.DetailView):
	model = Collection
	template_name = 'collection/detail_collection.html'


class update_collection(generic.UpdateView):
	model = Collection
	template_name = 'collection/update_collection.html'
	fields = ['title']
	success_url = reverse_lazy('dashboard')


class delete_collection(generic.DeleteView):
	model = Collection
	template_name = 'collection/delete_collection.html'
	success_url = reverse_lazy('dashboard')


