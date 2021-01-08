from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import views as auth_views

from rental.models.DBmodels.RentItem import RentItem


@login_required(redirect_field_name='',login_url='/')
def get_choice_view(request):
    # todo get items which are available in dorm
    # print(RentItem.objects.all().values("name"))


    return render(request, "panel/choice.html")