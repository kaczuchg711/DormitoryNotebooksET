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
    def decide_about_rent(cls, request):
        print_Post(request)
        if request.POST["submit"] == "turnBack":
            cls.turn_back(request)
        elif request.POST["submit"] == "rentItem":
            cls.rent(request)

        return redirect("rent")

    @classmethod
    def turn_back(cls, request):
        t = time.localtime()
        returnHour = time.strftime("%H:%M:%S", t)
        itemToRentName = request.session["name_item_to_rent"]
        rentItemLog = cls.objects.filter(user=request.user, item__name=itemToRentName, returnHour=None)[0]
        rentItemLog.returnHour = returnHour
        rentItemLog.save()

        itemToRent = Item.objects.filter(id=rentItemLog.item_id)[0]
        itemToRent.isAvailable = True
        itemToRent.save()

        request.session["last_rent_item"] = itemToRent.name

    @classmethod
    def rent(cls, request):

        user, dorm, itemName, rentalDate, rentHour = cls._collect_data_for_RentItem(request)

        itemToRent = Item.objects.filter(dorm=dorm, name=itemName, number=request.POST["items"])[0]

        rentItem = cls(user=user, dorm=dorm, item_id=itemToRent.id, rentalDate=rentalDate, rentHour=rentHour)
        cls(user=user, dorm=dorm, item_id=itemToRent.id, rentalDate=rentalDate, rentHour=rentHour)
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

        if len(RentItem.objects.filter(user=request.user, returnHour=None,
                                       item_id__in=ItemsWithFalseIsAvaibleids)) == 0:
            return False
        areAvaible = change_QuerySet_from_db_to_list(areAvaible, "isAvailable")

        if False in areAvaible:
            return True
        else:
            return False
