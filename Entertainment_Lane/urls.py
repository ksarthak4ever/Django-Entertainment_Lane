"""Entertainment_Lane URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from collection import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my_collection/create', views.create_collection.as_view(), name='create_collection'),
    path('my_collection/<int:pk>/', views.detail_collection.as_view(), name='detail_collection'),
    path('my_collection/<int:pk>/update', views.update_collection.as_view(), name='update_collection'),
    path('my_collection/<int:pk>/delete', views.delete_collection.as_view(), name='delete_collection'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
