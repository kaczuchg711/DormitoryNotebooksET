from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

from organizations.models import Organization
from organizations import views as organizationsView


def get_home_view(request):
    organization_id = request.session.get('organization_id')

    if request.session.get('organization_id') is None:
        return organizationsView.get_organization_view(request)

    organization = Organization.objects.filter(id=organization_id)[0]
    organizations_dorms_names = organization.get_dorms_names()

    context = {
        'organizationLogoPath': "img/" + organization.acronym + "_logo.png",
        'organizations_dorms_names': organizations_dorms_names
    }
    return render(request, template_name='security/home.html', context=context)


def set_organization(request):
    organizationAcronym = request.POST.get('organization')
    if Organization.organization_in_db(organizationAcronym):
        organization = Organization.objects.filter(acronym=organizationAcronym)[0]
        request.session['organization_id'] = organization.get_id()
        return redirect('/')
    else:
        return redirect('organization')


def get_choice_view_if_data_ok(request):
    user = _get_authenticate_user(request)
    if user is not None:
        login(request, user)
        return redirect('/choice')
    else:
        messages.add_message(request, messages.INFO, "wrong password or e-mail")
        return redirect('/')


def _get_authenticate_user(request):
    username = request.POST['username']
    password = request.POST['password']
    return authenticate(request, username=username, password=password)
