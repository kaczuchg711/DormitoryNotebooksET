from datetime import time, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms import models
from django.shortcuts import redirect, render
from django.contrib import messages
from ipware import get_client_ip

from global_fun import print_with_enters
from organizations.models import Organization, Dorm
from organizations import views as organizationsView
from rental.models.NonDBmodels.BlockedUserSetter import BlockedUserSetter

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

    import time as timep
    client_ip, is_routable = get_client_ip(request)

    blockedUserSetter = BlockedUserSetter(client_ip)
    t = timep.localtime()
    actual_time = timep.strftime("%H:%M:%S", t)
    rows = BlockedUsers.objects.filter(ip=client_ip)
    # check user ip is in blocked list and check that user have to wait
    # check blocked time passed
    if blockedUserSetter.have_user() and blockedUserSetter.user_is_blocked():
        print_with_enters(blockedUserSetter.user_is_blocked())
        if not blockedUserSetter.block_time_passed():
            messages.add_message(request, messages.INFO, "too many attempts wait a moment")
            return False
        else:
            blockedUserSetter.delete_user_from_blocked_list()
    # todo clean this mebe simble change row[0] to object?
    if user is not None:
        if user.is_superuser:
            dormName = request.POST['dorms']
            request.session['dorm_id'] = Dorm.objects.filter(name=dormName)[0].id
            return True

        dormName = request.POST['dorms']
        request.session['dorm_id'] = Dorm.objects.filter(name=dormName)[0].id
        organizationId = request.session.get("organization_id")
        try:
            LoginUser = create_user_to_log_in(user)
        except ValueError:
            messages.add_message(request, messages.INFO, "wrong data")
            #
            return False
        if LoginUser.check_requirement(user, organizationId, dormName):
            return True
    messages.add_message(request, messages.INFO, "wrong data")

    if len(rows) == 0:
        user_to_block = BlockedUsers(login=request.POST['email'], count=1, ip=client_ip, blocked=False, blocking_time=actual_time)
        user_to_block.save()
    else:
        rows[0].count = str(int(rows[0].count) + 1)
        if rows[0].count == "3":
            rows[0].blocked = True
            rows[0].blocking_time = actual_time
        rows[0].save()
    return False
