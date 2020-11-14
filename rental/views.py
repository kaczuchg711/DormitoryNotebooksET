from MySQLdb.converters import NoneType
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from rental.models.DBmodels.RentItem import RentItem
from rental.models.DBmodels.Item import Item
from rental.forms import RentForm


@login_required(redirect_field_name='', login_url='/')
def create_base_view(request):
    # todo check this itemName the users are realy bad
    itemName = request.POST['button']
    dormId = request.session.get('dorm_id')
    # todo change this when you do this fun with available items

    itemsInDorm = Item.objects.filter(dorm_id=dormId,name=itemName)
    itemsId = list()
    for item in itemsInDorm:
        itemsId.append(item.id)

    rentItemLogs = RentItem.objects.filter(dorm_id=dormId, item_id__in=itemsId)
    print(rentItemLogs)
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

    rentData = zip(dates, userNames, userLastNames, roomUserNumbers, rentHour, returnHour)

    availableItems = Item.objects.filter(dorm_id=dormId, isAvailable=True)

    form = RentForm(availableItems)

    context = {
        'rentData': rentData,
        'availableItemsForm': form
    }
    return render(request, "rental/rental.html", context)
