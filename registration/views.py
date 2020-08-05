from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

def get_home_view_if_data_ok(request):
    user = _get_authenticate_user(request)
    if user is not None:
        login(request, user)
        return redirect('/home')
    else:
        messages.add_message(request, messages.INFO, "wrong password or e-mail")
        return redirect('/')

def _get_authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    return authenticate(request, username=username, password=password)

def get_organization_view(request):
    return render(request,template_name='registration/organization.html')