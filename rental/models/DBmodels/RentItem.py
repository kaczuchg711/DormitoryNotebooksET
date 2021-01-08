import time

from MySQLdb import Date, Time
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError

from global_fun import print_with_enters, print_Post, print_session
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

    @staticmethod
    def rent(request: WSGIRequest):

        print_Post(request)

        user, dorm, itemName, rentalDate, rentHour = RentItem._collect_data_for_RentItem(request)

        itemToRent = Item.objects.filter(dorm=dorm, name=itemName, number=request.POST["items"])[0]

        rentItem = RentItem(user=user, dorm=dorm, item_id=itemToRent.id, rentalDate=rentalDate, rentHour=rentHour)
        RentItem(user=user, dorm=dorm, item_id=itemToRent.id, rentalDate=rentalDate, rentHour=rentHour)
        rentItem.save()
        itemToRent.isAvailable = False
        itemToRent.save()

        request.session["last_rent_item"] = itemName

        return redirect('rent')

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

        try:
            number = request.POST["item_number"]
        except MultiValueDictKeyError:
            return False

        dormID = request.session.get("dorm_id")
        dorm = Dorm.objects.filter(id=dormID)[0]
        itemName = "vacuum cleaner"

        if Item.objects.filter(dorm=dorm, name=itemName, number=number) is None:
            return False
        else:
            return True
