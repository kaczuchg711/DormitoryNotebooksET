import time
from datetime import datetime, tzinfo

from MySQLdb import Date, Time
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.shortcuts import redirect

from organizations.models import Dorm
from users.models import CustomUser


class RentItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
    itemName = models.CharField(max_length=255)
    rentalDate = models.DateField(default=None)
    rentHour = models.TimeField(default=None)
    returnHour = models.TimeField(default=None, null=True)

    @staticmethod
    def rent(request:WSGIRequest):
        #   Todo
        #   itemName, data, name , surname , dormId, userID
        user = request.user
        dormID = request.session.get("dorm_id")
        dorm = Dorm.objects.filter(id=dormID)[0]
        # Todo dynamic itemName
        itemName = "vacuum cleaner"
        rentalDate = Date.today()
        t = time.localtime()
        rentHour = time.strftime("%H:%M:%S", t)
        # .strftime("%H:%M:%S")
        # print("siema")
        # print("siema")
        # print("siema")
        # print("siema")
        # print(rentHour)
        # print("siema")
        # print("siema")
        # print("siema")
        # print("siema")


        rentItem = RentItem(user=user,dorm=dorm,itemName=itemName,rentalDate=rentalDate,rentHour=rentHour)
        rentItem.save()


        return redirect('rent')


    #   data, imie, nazwisko , nr pokoju , godzine pobrania, godzine oddania
