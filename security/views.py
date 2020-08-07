from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

from security.models import Organization


def get_home_view(request):
    print(request.session.get('organization'))
    if request.session.get('organization') is None:
        return get_organization_view(request)

    context = {
        # 'organizationName':
        'organizationLogoPath': "img/" + request.session.get('organization') + "_logo.png"
    }
    return render(request, template_name='security/home.html', context=context)


def set_organization(request):
    # Todo validation we have this organization in db ?
    request.session['organization'] = request.POST.get('organization')
    return redirect('/')


def get_organization_view(request):
    context = _prepare_organization_data(request)
    print(context)
    return render(request, template_name='security/organization.html', context=context)


def _prepare_organization_data(request):
    querySet = Organization.objects.values('acronym')
    acronyms = [d['acronym'] for d in [x for x in querySet]]
    imgPath = ["img/" + path + "_logo.png" for path in acronyms]
    context = {
        'organizationsAcronym': acronyms,
        'organizations_logo_path': imgPath,
        'organizationsAcronymsAndPathToIMG': zip(acronyms,imgPath)
    }
    return context


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
