from django.db import models
from ipware import get_client_ip

from organizations.models import Dorm
from users.models import CustomUser

# blokada gdy poda 3 razy zle hasło 5 razy zly login
class BlockedUsers(models.Model):
    login = models.TextField(default="")
    count = models.TextField(default=0)
    ip = models.TextField(default="")
    blocked = models.BooleanField(default=False)
    blocking_time = models.TimeField(default="00:00:00")

    @staticmethod
    def client_ip_is_in_blockedUsers():
        pass

