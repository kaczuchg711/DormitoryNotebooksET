from django.shortcuts import render

# Create your views here.
from security.models import User_Associate_with_Organization


def create_base_view(request):
    return render(request, "rental/rental.html")