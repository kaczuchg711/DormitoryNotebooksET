from MySQLdb.converters import NoneType
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.datastructures import MultiValueDictKeyError

from global_fun import print_with_enters
from rental.models.DBmodels.RentItem import RentItem
from rental.models.DBmodels.Item import Item
from rental.forms import RentForm, TurnBackForm


@login_required(redirect_field_name='', login_url='/')
def create_base_view(request):
    # todo check itemName. The users are really bad

    try:
        itemName = _get_item_name(request)
    except KeyError:
        return redirect("choice")

    dormId = request.session.get('dorm_id')
    itemsIds = _get_items_list(dormId, itemName)
    rentData = _prepare_rent_data(dormId, itemsIds)
    form, buttonString, formAction = _get_form_information_depend_on_avaiableItems(request, dormId, itemName)

    context = {
        'rentData': rentData,
        'availableItemsForm': form,
        'buttonString': buttonString,
        'formAction': formAction
    }
    return render(request, "rental/rental.html", context)


def _get_item_name(request):
    # user choose item for rent
    try:
        itemName = request.POST['button']
        request.session['name_item_to_rent'] = itemName
        return itemName
    except MultiValueDictKeyError:
        try:
            # user reload page
            itemName = request.session["last_rent_item"]
            return itemName
        except KeyError:
            # user want enter rent page from url
            return redirect("choice")


def _get_items_list(dormId, itemName):
    itemsInDorm = Item.objects.filter(dorm_id=dormId, name=itemName)
    itemsId = [item.id for item in itemsInDorm]
    return itemsId


def _prepare_rent_data(dormId, itemsIds):
    rentItemLogs = RentItem.objects.filter(dorm_id=dormId, item_id__in=itemsIds)

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
    return rentData


def _get_form_information_depend_on_avaiableItems(request, dormId, itemName):
    availableItems = Item.objects.filter(dorm_id=dormId, isAvailable=True, name=itemName)

    if RentItem.user_already_renting(request):
        form = TurnBackForm()
        buttonString = "zwróć"
        formAction = "turnBack"
    else:
        form = RentForm(availableItems)
        buttonString = "wypożycz"
        formAction = "rentItem"

    return form, buttonString, formAction
