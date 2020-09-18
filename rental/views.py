from django.shortcuts import render

# Create your views here.
from rental.models.DBmodels.RentItem import RentItem
from users.models import CustomUser


def create_base_view(request):
    dormId = request.session.get('dorm_id')
    itemName = "vacuum cleaner"
    rentItemLogs = RentItem.objects.filter(dorm_id=dormId, itemName=itemName)

    dates = [row.rentalDate.isoformat() for row in rentItemLogs]
    users = [i.user for i in rentItemLogs]
    userNames = [x.first_name for x in users]
    userLastNames = [x.last_name for x in users]
    roomUserNumbers = [x.room_number for x in users]
    rentHour = [row.rentHour for row in rentItemLogs]
    returnHour = [row.returnHour for row in rentItemLogs]

    aaaa = zip(dates,userNames,userLastNames,roomUserNumbers,rentHour,returnHour)

    context = {
        'aaaa': aaaa
    }
    return render(request, "rental/rental.html",context)
