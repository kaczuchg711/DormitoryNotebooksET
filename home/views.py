from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import views as auth_views

@login_required(redirect_field_name='',login_url='/')
def show_home(request):
    context = {'user': request.user.username}
    return render(request, "home/home.html", context)