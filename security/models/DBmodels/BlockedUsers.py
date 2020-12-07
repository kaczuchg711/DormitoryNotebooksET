from django.db import models
from ipware import get_client_ip

from datetime import timedelta, time
import time as basic_time

from global_fun import get_actual_time
from organizations.models import Dorm
from users.models import CustomUser

class BlockedUsers(models.Model):
    login = models.TextField(default="")
    count = models.TextField(default=0)
    ip = models.TextField(default="")
    blocked = models.BooleanField(default=False)
    blocking_time = models.TimeField(default="00:00:00")
    maxAttemptsNumber = 3

    def block_time_passed(self):
        t = basic_time.localtime()
        actual_time = basic_time.strftime("%H:%M:%S", t)
        t1 = timedelta(hours=time.fromisoformat(actual_time).hour, minutes=time.fromisoformat(actual_time).minute
                       , seconds=time.fromisoformat(actual_time).second)
        t2 = timedelta(hours=self.blocking_time.hour, minutes=self.blocking_time.minute
                       , seconds=self.blocking_time.second)
        min_waiting_seconds = 5

        return False if t1.total_seconds() - t2.total_seconds() < min_waiting_seconds else True

    def increase_number_of_wrong_attempts(self):
        self.count = str(int(self.count) + 1)
        self.save()

    def check_count_breach_and_block(self):
        if self.count == str(self.maxAttemptsNumber):
            self._block()

    def _block(self):
        t = basic_time.localtime()
        actual_time = basic_time.strftime("%H:%M:%S", t)
        self.blocked = True
        self.blocking_time = actual_time
        self.save()

    def delete_user_from_blocked_list(self):
        self.delete()

    @staticmethod
    def delete_user_from_blocked_list_by_ip(client_ip):
        blockedUser = BlockedUsers.objects.filter(ip=client_ip)
        blockedUser.delete()

    @staticmethod
    def create_blocked_user(request):
        actual_time = get_actual_time()
        client_ip, is_routable = get_client_ip(request)
        blockedUser = BlockedUsers(login=request.POST['email'], count=1, ip=client_ip, blocked=False, blocking_time=actual_time)
        blockedUser.save()


