from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from django.contrib import messages

from organizations.models import Organization, Dorm
from organizations import views as organizationsView
from django import forms

from security.forms import LoginForm
from security.models import User_Associate_with_Dorm, User_Associate_with_Organization, create_user_to_log_in


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
        form.save()

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



    if _data_ok(request, user):
        login(request, user)

        return redirect("/choice")
    else:
        return redirect("/")


def _data_ok(request, user:User):
    # Todo if is supervisor or porter can go to organization with out dorm checking
    #  learn permission in django
    dormName = request.POST['dorms']
    organizationId = request.session.get("organization_id")


    print(type(create_user_to_log_in(user)))


    # if user is not None:
    #     if Dorm.dorm_exist(dormName):
    #         dorm_id = Dorm.get_dorm_id(dormName)
    #         if User_Associate_with_Dorm.association_exist(dorm_id, user.id) or user.id == 4 and \
    #                 User_Associate_with_Organization.association_exist(organizationId, user.id):
    #             return True
    #         elif user.is_superuser:
    #             return True
    #         else:
    #             messages.add_message(request, messages.INFO, "wrong association with dorm or organization")
    #             return False
    #     else:
    #         messages.add_message(request, messages.INFO, "wrong Dorm name")
    #         return False
    # messages.add_message(request, messages.INFO, "wrong login or password")
    # return False

    if user is not None:
        if user.is_superuser:
            return True

        LoginUser = create_user_to_log_in(user)
        if LoginUser.check_requirement(user,organizationId,dormName):
            return True
    messages.add_message(request, messages.INFO, "wrong data")
    return False


def _get_authenticate_user(request):
    username = request.POST['login']
    password = request.POST['password']
    return authenticate(request, username=username, password=password, )
