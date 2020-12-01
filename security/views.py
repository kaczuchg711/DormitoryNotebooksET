

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms import models
from django.shortcuts import redirect, render
from django.contrib import messages
from ipware import get_client_ip

from global_fun import print_with_enters
from organizations.models import Organization, Dorm
from organizations import views as organizationsView

from security.forms import LoginForm
from security.models.fun import create_user_to_log_in
from security.models.DBmodels.BlockedUsers import BlockedUsers


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


def _get_authenticate_user(request):
    email = request.POST['email']
    password = request.POST['password']
    return authenticate(request, email=email, password=password)


def _data_ok(request, user: User):

    client_ip, is_routable = get_client_ip(request)

    try:
        blockedUser = BlockedUsers.objects.filter(ip=client_ip)[0]
    except IndexError:
        blockedUser = None

    if blockedUser is not None and blockedUser.blocked:
        if not blockedUser.block_time_passed():
            messages.add_message(request, messages.INFO, "too many attempts wait a moment")
            return False
        else:
            blockedUser.delete_user_from_blocked_list()

    if user is not None:
        dormName = request.POST['dorms']
        request.session['dorm_id'] = Dorm.objects.filter(name=dormName)[0].id
        if user.is_superuser:
            return True

        organizationId = request.session.get("organization_id")
        try:
            LoginUser = create_user_to_log_in(user)
        except ValueError:
            messages.add_message(request, messages.INFO, "wrong data")
            return False

        if LoginUser.check_requirement(user, organizationId, dormName):
            return True


    if blockedUser is None:
        BlockedUsers.create_blocked_user(request)
    else:
        blockedUser.increase_number_of_wrong_attempts()
        blockedUser.check_count_breach_and_block()

    messages.add_message(request, messages.INFO, "wrong data")
    return False
