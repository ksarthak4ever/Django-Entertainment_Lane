from django.shortcuts import render, redirect
from django.urls import reverse_lazy #used to redirect to homepage when someone signs up sucessfully.
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login 
from .models import Collection,Video
from .forms import VideoForm, SearchForm
from django.http import Http404
from django.forms.utils import ErrorList 


import urllib #importing this library to parse the youtube video url and get it's id
import requests

YOUTUBE_API_KEY = 'AIzaSyAE79s9L9lU-OKs8fqa8R7HS-a0NDr2UPo' #put it in environment variables during production


def home(request):
	return render(request, 'collection/home.html')

def dashboard(request):
	return render(request, 'collection/dashboard.html')

def add_video(request, pk):
	form = VideoForm()
	search_form = SearchForm()
	collection = Collection.objects.get(pk=pk)
	if not collection.user == request.user:
		raise Http404

	if request.method == 'POST':
		form = VideoForm(request.POST)
		
		if form.is_valid():
			video = Video()
			video.collection = collection
			video.url = form.cleaned_data['url']
			parsed_url = urllib.parse.urlparse(video.url) #parsing the youtube url
			video_id = urllib.parse.parse_qs(parsed_url.query).get('v') #as v is the pararmeter that stores the youtube id in the url
			
			if video_id:
				video.youtube_id = video_id[0] #as video_id returns a list
				response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet&id={ video_id[0] }&key={ YOUTUBE_API_KEY }')
				json = response.json() #converting response into json
				title = json['items'][0]['snippet']['title']
				video.title = title
				video.save()
				return redirect('detail_collection', pk)
			else:
				errors = form._errors.setdefault('url', ErrorList())
				errors.append('Needs to be a YouTube URL')

	return render(request, 'collection/add_video.html', {'form':form, 'search_form':search_form, 'collection':collection})


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


