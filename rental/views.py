from django.shortcuts import render

# Create your views here.

def create_base_view(request):
    return render(request, "rental/rental.html")