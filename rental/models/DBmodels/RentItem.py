import time

from MySQLdb import Date, Time
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError

from global_fun import print_with_enters, print_Post, print_session, change_QuerySet_from_db_to_list
from organizations.models import Dorm
from rental.models.DBmodels.Item import Item
from users.models import CustomUser


class RentItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)
    rentalDate = models.DateField(default=None)
    rentHour = models.TimeField(default=None)
    returnHour = models.TimeField(default=None, null=True)

    @classmethod
    def decideAboutRent(cls, request: WSGIRequest):
        if request.POST["submit"] == "zwróć":
            cls.turn_back(request)
        if request.POST["submit"] == "wypożycz":
            cls.rent(request)

        return redirect("rent")

    @staticmethod
    def turn_back(request):
        t = time.localtime()
        returnHour = time.strftime("%H:%M:%S", t)
        rentItemlog = \
            RentItem.objects.filter(user=request.user, item__name=request.session["name_item_to_rent"],
                                    returnHour=None)[0]
        rentItemlog.returnHour = returnHour
        rentItemlog.save()

        itemsToRent = Item.objects.filter(id=rentItemlog.item_id)
        print_with_enters(itemsToRent)
        itemToRent = Item.objects.filter(id=rentItemlog.item_id)[0]
        itemToRent.isAvailable = True
        itemToRent.save()

        request.session["last_rent_item"] = itemToRent.name

    @staticmethod
    def rent(request: WSGIRequest):

        user, dorm, itemName, rentalDate, rentHour = RentItem._collect_data_for_RentItem(request)

        itemToRent = Item.objects.filter(dorm=dorm, name=itemName, number=request.POST["items"])[0]

        rentItem = RentItem(user=user, dorm=dorm, item_id=itemToRent.id, rentalDate=rentalDate, rentHour=rentHour)
        RentItem(user=user, dorm=dorm, item_id=itemToRent.id, rentalDate=rentalDate, rentHour=rentHour)
        rentItem.save()
        itemToRent.isAvailable = False
        itemToRent.save()

        request.session["last_rent_item"] = itemName

    @staticmethod
    def _collect_data_for_RentItem(request):
        user = request.user
        dormID = request.session.get("dorm_id")
        dorm = Dorm.objects.filter(id=dormID)[0]
        itemName = request.session['name_item_to_rent']

        rentalDate = Date.today()
        t = time.localtime()
        rentHour = time.strftime("%H:%M:%S", t)

        return user, dorm, itemName, rentalDate, rentHour

    @staticmethod
    def user_already_renting(request: WSGIRequest):

        dormID = request.session.get("dorm_id")
        dorm = Dorm.objects.filter(id=dormID)[0]
        itemName = request.session['name_item_to_rent']

        areAvaible = Item.objects.filter(dorm=dorm, name=itemName)
        ItemsWithFalseIsAvaibleids = areAvaible.filter(isAvailable=False).values_list("id")

        if len(RentItem.objects.filter(user=request.user, returnHour=None, item_id__in=ItemsWithFalseIsAvaibleids)) == 0:
            return False
        areAvaible = change_QuerySet_from_db_to_list(areAvaible, "isAvailable")

        if False in areAvaible:
            return True
        else:
            return False
