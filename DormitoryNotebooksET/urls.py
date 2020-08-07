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

from security import views as securityViews
from choice import views as choiceViews
from rental import views as rentalViews

urlpatterns = [
    # path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='start Page'),
    # path('choice/', homeViews.show_home, name='choice' ),
    # path('logout/', auth_views.LogoutView.as_view(template_name='security/choice.html'), name='logout'),
    # path('login/', securityViews.get_home_view_if_data_ok, name='login'),
    #


    # path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='start Page'),
    path('', securityViews.get_home_view, name='index'),
    path('admin/', admin.site.urls),
    path('login/', securityViews.get_choice_view_if_data_ok, name="login"),
    path('logout/', authViews.LogoutView.as_view(template_name='security/home.html'), name='logout'),
    path('choice/', choiceViews.get_choice_view, name='choice'),
    path('rent/', rentalViews.create_base_view, name='rent'),
    path('organization/', securityViews.get_organization_view, name='organization'),
    path('set_organization/', securityViews.set_organization, name='set_organization'),
]
