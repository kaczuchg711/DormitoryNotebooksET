from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    room_number = models.CharField(max_length=10,default=None,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def is_in_any_group(self):
        user_groups = self.groups.all()
        if len(user_groups) == 0:
            return False
        return True

    def is_in_group(self, group_name):
        groups = Group.objects.all()

        a = groups.filter(name=group_name)
        b = self.groups.all()
        if all(x in a for x in b):
            return True
        return False


