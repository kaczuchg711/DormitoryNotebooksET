"""DormitoryNotebooksET URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.shortcuts import redirect, render
from django.urls import path
from django.contrib.auth import views as auth_views

from home import views as homeViews
from rental import views as rentalViews
from registration import views as registrationViews


urlpatterns = [
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='start Page'),
    path('home/', homeViews.show_home, name='login' ),
    path('admin/', admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/login.html'), name='logout'),
    path('login/', registrationViews.log_in, name='login' ),
    path('rent/', rentalViews.create_base_view, name='rent' ),
]


