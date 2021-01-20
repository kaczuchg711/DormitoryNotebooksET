from MySQLdb.converters import NoneType
from django.shortcuts import render, redirect
from MySQLdb import Date

# Create your views here.
from breakdowns.forms import BreakdownForm
from breakdowns.models import Breakdowns
from global_fun import *


def create_breakdown_view(request):
    isPorter = True if request.user.is_in_group("porters") else False
    # todo create buttons to set breakdown as removed
    breakdownData = _prepare_breakdown_data(request)
    form = BreakdownForm()

    context = {
        'breakdownData': breakdownData,
        'form': form,
        'isPorter': isPorter
    }

    return render(request, "breakdowns/breakdowns.html", context=context)


def request_breakdown(request):
    print_Post(request)
    print_session(request)

    requestDate, user_id, description, dorm_id = _prepare_breakdown_request_data(request)

    breakdown = Breakdowns(requestDate=requestDate, user_id=user_id, description=description, isSolved=False,
                           dorm_id=dorm_id)
    breakdown.save()

    return redirect(create_breakdown_view)


def _prepare_breakdown_request_data(request):
    description = request.POST["description"]
    requestDate = Date.today()
    user_id = request.user.id
    dorm_id = request.session["dorm_id"]
    return requestDate, user_id, description, dorm_id


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
    stateds = ["do usunięcia" if stade is False else "usunięta" for stade in stateds_db]
    # form.
    bt = ["<button>x</button>", "<button>x</button>", "<button>x</button>"]
    rentData = zip(dates, userNames, userLastNames, roomUserNumbers, description, stateds,bt)
    return rentData