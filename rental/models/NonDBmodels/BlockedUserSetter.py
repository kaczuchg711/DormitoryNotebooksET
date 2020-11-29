from datetime import timedelta, time
import time as basic_time

from security.models.DBmodels.BlockedUsers import BlockedUsers


class BlockedUserSetter:

    def __init__(self, client_ip):
        rows = BlockedUsers.objects.filter(ip=client_ip)
        if (len(rows) != 0):
            self.blockedUser = BlockedUsers.objects.filter(ip=client_ip)[0]

    def have_user(self):
        return hasattr(self, "blockedUser")

    def user_have_maximum_number_of_attempts(self):

        if self.blockedUser.count == '3':
            return True
        else:
            return False

    def user_is_blocked(self):
        return self.blockedUser.blocked
    def block_time_passed(self):

        t = basic_time.localtime()
        actual_time = basic_time.strftime("%H:%M:%S", t)
        t1 = timedelta(hours=time.fromisoformat(actual_time).hour, minutes=time.fromisoformat(actual_time).minute
                       , seconds=time.fromisoformat(actual_time).second)
        t2 = timedelta(hours=self.blockedUser.blocking_time.hour, minutes=self.blockedUser.blocking_time.minute
                       , seconds=self.blockedUser.blocking_time.second)
        min_waiting_seconds = 5

        return False if t1.total_seconds() - t2.total_seconds() < min_waiting_seconds else True

    def delete_user_from_blocked_list(self):
        self.blockedUser.delete()
