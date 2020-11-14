import time

from MySQLdb import Date, Time
from django.core.handlers.wsgi import WSGIRequest
from django.db import models
from django.shortcuts import redirect

from organizations.models import Dorm
from rental.models.DBmodels.Item import Item
from users.models import CustomUser


class RentItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dorm = models.ForeignKey(Dorm, on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE,default=None)
    rentalDate = models.DateField(default=None)
    rentHour = models.TimeField(default=None)
    returnHour = models.TimeField(default=None, null=True)

    @staticmethod
    def rent(request: WSGIRequest):
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

        rentItem = RentItem(user=user, dorm=dorm, item_id=0, rentalDate=rentalDate, rentHour=rentHour)
        rentItem.save()

        return redirect('rent')
