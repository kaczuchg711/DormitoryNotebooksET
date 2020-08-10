from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

from organizations.models import Organization
from organizations import views as organizationsView


def get_home_view(request):
    organization_id = request.session.get('organization_id')

    if request.session.get('organization_id') is None:
        return organizationsView.get_organization_view(request)

    context = _prepare_context_data(organization_id)
    return render(request, template_name='security/home.html', context=context)

def _prepare_context_data(organization_id):
    organization = Organization.objects.filter(id=organization_id)[0]
    organizations_dorms_names = organization.get_dorms_names()

    context = {
        'organizationLogoPath': "img/" + organization.acronym + "_logo.png",
        'organizations_dorms_names': organizations_dorms_names
    }
    return context





def log_in(request):
    user = _get_authenticate_user(request)

    if _data_ok(user):
        login(request, user)
        return redirect("/choice")
    else:
        messages.add_message(request, messages.INFO, "wrong password or e-mail")
        return redirect("/")


def _data_ok(user):
    if user is not None:
        return True
    else:
        return False


def _get_authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    return authenticate(request, username=username, password=password)
