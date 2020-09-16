from django.contrib.auth.models import Group

from security.models.NonDBmodels.Student import Student
from security.models.NonDBmodels.Supervisor import Supervisor


def create_user_to_log_in(user):
    user_groups = user.groups.all()

    if len(user_groups) == 0:
        raise ValueError
    elif _user_in_group(user_groups, "supervisors"):
        return Supervisor()
    elif _user_in_group(user_groups, "students"):
        return Student()
    else:
        raise ValueError

# Todo add this to user class
def _user_in_group(user_groups, group_name):
    groups = Group.objects.all()
    return all(x in groups.filter(name=group_name) for x in user_groups)
