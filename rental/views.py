from MySQLdb.converters import NoneType
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from rental.models.DBmodels.RentItem import RentItem
from rental.models.DBmodels.Item import Item
from users.models import CustomUser
from global_fun import print_with_enters
from global_fun import change_QuerySet_from_db_to_list



@login_required(redirect_field_name='',login_url='/')
def create_base_view(request):
    itemName = request.POST['button']
    dormId = request.session.get('dorm_id')
    rentItemLogs = RentItem.objects.filter(dorm_id=dormId, itemName=itemName)

    dates = [row.rentalDate.isoformat() for row in rentItemLogs]
    users = [i.user for i in rentItemLogs]
    userNames = [x.first_name for x in users]
    userLastNames = [x.last_name for x in users]
    roomUserNumbers = [x.room_number for x in users]
    rentHour = [row.rentHour.isoformat() for row in rentItemLogs if row.rentHour is not None]

    returnHour = []
    for row in rentItemLogs:
        if type(row.returnHour) is not NoneType:
            returnHour.append(row.returnHour.isoformat())
        else:
            returnHour.append("")
    # Todo load available items


    rentData = zip(dates, userNames, userLastNames, roomUserNumbers, rentHour, returnHour)

    availableItems = Item.objects.filter(dorm_id=dormId,isAvailable=True)

    numbers = list()
    names = list()
    for item in availableItems:
        numbers.append(item.number)
        names.append(item.name)

    availableItemsData = zip(numbers,names)

    context = {
        'rentData': rentData,
        'availableItems': availableItemsData
    }
    return render(request, "rental/rental.html", context)