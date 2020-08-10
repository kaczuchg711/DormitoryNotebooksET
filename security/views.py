from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

from organizations.models import Organization, Dorm
from organizations import views as organizationsView
from django import forms

from security.forms import LoginForm
from security.models import User_Associate_with_Dorm, User_Associate_with_Organization


def get_home_view(request):
    organization_id = request.session.get('organization_id')

    if request.session.get('organization_id') is None:
        return organizationsView.get_organization_view(request)

    context = _prepare_context_data(organization_id)
    return render(request, template_name='security/home.html', context=context)


def _prepare_context_data(organization_id):
    organization = Organization.objects.filter(id=organization_id)[0]
    organizations_dorms_names = organization.get_dorms_names()

    form = LoginForm(organizations_dorms_names)
    if form.is_valid():
        context = {
            'organizationLogoPath': "img/" + organization.acronym + "_logo.png",
            'organizations_dorms_names': organizations_dorms_names,
            'form': form,
        }
        return context
    else:
        context = {
            'organizationLogoPath': "img/" + organization.acronym + "_logo.png",
            'organizations_dorms_names': organizations_dorms_names,
            'form': form,
        }
        return context


def log_in(request):
    user = _get_authenticate_user(request)
    dormName = request.POST['dorms']
    organizationId = request.session.get("organization_id")

    if _data_ok(user, dormName, organizationId):
        login(request, user)
        return redirect("/choice")
    else:
        messages.add_message(request, messages.INFO, "wrong password or e-mail")
        return redirect("/")


def _data_ok(user, dormName, organizationId):
    # Todo if is supervisor or porter can go to organization
    if user is not None:
        # Todo make this clean this dorm exist ?
        dorms = list(Dorm.objects.filter(name=dormName))
        if len(dorms) != 0:
            dorm_id = dorms[0].get_id()
            if len(User_Associate_with_Dorm.objects.filter(id_dorm_id=dorm_id, id_user=user.id)) != 0 and \
                    len(User_Associate_with_Organization.objects.filter(id_organization_id=organizationId, id_user_id=user.id)) != 0:
                return True
            elif user.is_superuser:
                return True
    return False


def _get_authenticate_user(request):
    username = request.POST['login']
    password = request.POST['password']
    return authenticate(request, username=username, password=password, )
