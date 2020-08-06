from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import views as auth_views

@login_required(redirect_field_name='',login_url='/')
def get_choice_view(request):
    return render(request, "home/choice.html")