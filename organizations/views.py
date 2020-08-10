from django.shortcuts import render, redirect

# Create your views here.

from organizations.models import Organization

def get_organization_view(request):
    context = _prepare_organization_data(request)
    return render(request, template_name='security/organization.html', context=context)



def _prepare_organization_data(request):
    imgPath = Organization.get_every_organizations_paths_to_logos()
    acronyms = Organization.get_every_organizations_acronyms()
    context = {
        'organizationsAcronym': acronyms,
        'organizations_logo_path': imgPath,
        'organizationsAcronymsAndPathToIMG': zip(acronyms,imgPath)
    }
    return context