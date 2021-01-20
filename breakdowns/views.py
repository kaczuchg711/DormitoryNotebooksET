from MySQLdb.converters import NoneType
from django.shortcuts import render

# Create your views here.
from breakdowns.models import Breakdowns
from global_fun import *


def create_breakdown_view(request):
    breakdownData = _prepare_breakdown_data(request)

    context = {
        'breakdownData': breakdownData,
    }

    return render(request, "breakdowns/breakdowns.html", context=context)


def _prepare_breakdown_data(request):
    dormId = request.session.get('dorm_id')
    breakdownsLogs = Breakdowns.objects.filter(dorm_id=dormId)
    dates = [row.requestDate.isoformat() for row in breakdownsLogs]
    users = [row.user for row in breakdownsLogs]
    userNames = [user.first_name for user in users]
    userLastNames = [user.last_name for user in users]
    roomUserNumbers = [user.room_number for user in users]
    description = [row.description for row in breakdownsLogs]
    stateds_db = [row.isSolved for row in breakdownsLogs]
    print_with_enters(stateds_db)
    stateds = ["do usunięcia" if stade is False else "usunięta" for stade in stateds_db]
    rentData = zip(dates, userNames, userLastNames, roomUserNumbers, description, stateds)
    return rentData
