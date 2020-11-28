"""DormitoryNotebooksET URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.choice, name='choice')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='choice')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as authViews

from rental.models.DBmodels.RentItem import RentItem
from security import views as securityViews
from organizations import views as organizationsViews
from choice import views as choiceViews
from rental import views as rentalViews
from organizations.models import Organization

urlpatterns = [
    # views
    path('', securityViews.get_home_view, name='index'),
    path('admin/', admin.site.urls),
    path('choice/', choiceViews.get_choice_view, name='choice'),
    path('rent/', rentalViews.create_base_view, name='rent'),
    path('organization/', organizationsViews.get_organization_view, name='organization'),
    # fun
    path('set_organization/', Organization.set_organization, name='set_organization'),
    path('login/', securityViews.log_in, name="login"),
    path('logout/', authViews.LogoutView.as_view(template_name='security/home.html'), name='logout'),
    path('rentItem/', RentItem.rent, name='rentItem')
]