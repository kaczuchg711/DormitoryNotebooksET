from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages

def log_in(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/home')
    else:
        messages.add_message(request, messages.INFO, "wrong password or e-mail")
        return redirect('/')
