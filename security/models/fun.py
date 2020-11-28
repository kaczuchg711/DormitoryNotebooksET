from django.contrib.auth.models import Group

from security.models.NonDBmodels.Student import Student
from security.models.NonDBmodels.Supervisor import Supervisor


def create_user_to_log_in(user):

    if not user.is_in_any_group():
        raise ValueError()
    elif user.is_in_group("supervisors"):
        return Supervisor()
    elif user.is_in_group("students"):
        return Student()
    else:
        raise ValueError
