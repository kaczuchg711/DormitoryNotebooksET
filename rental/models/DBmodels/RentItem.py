import time

from MySQLdb import Date, Time
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.shortcuts import redirect

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
        print("\n" * 3)
        print_Post(request)
        print("\n" * 3)
        print_session(request)
        print("\n" * 3)

        user = request.user
        dormID = request.session.get("dorm_id")
        dorm = Dorm.objects.filter(id=dormID)[0]
        # Todo dynamic itemName
        itemName = "vacuum cleaner"
        rentalDate = Date.today()
        t = time.localtime()
        rentHour = time.strftime("%H:%M:%S", t)

        itemId = Item.objects.filter(dorm=dorm, name=itemName, number=request.POST["items"])[0].id
        rentItem = RentItem(user=user, dorm=dorm, item_id=itemId, rentalDate=rentalDate, rentHour=rentHour)
        rentItem.save()

        request.session["last_rent_item"] = itemName

        return redirect('rent')

    @staticmethod
    def user_already_renting(request: WSGIRequest):
        user = request.user
        dormID = request.session.get("dorm_id")
        dorm = Dorm.objects.filter(id=dormID)[0]
        itemName = "vacuum cleaner"

        itemId = Item.objects.filter(dorm=dorm, name=itemName, number=request.POST["items"])[0].id

        return True
        # if (RentItem.objects.filter(user=user, , rentHour=None)[0] is not None ):
        #     return True
        # else:
        #     return False
