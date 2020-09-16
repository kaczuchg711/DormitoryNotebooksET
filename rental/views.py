from django.shortcuts import render

# Create your views here.


def create_base_view(request):
    # Todo have to make own user class
    # dormId = request.session.get('dorm_id')
    # itemName = "vacuum cleaner"
    # rentItemLogs = RentItem.objects.filter(dorm_id=dormId, itemName=itemName)
    # dates = [row.rentalDate for row in rentItemLogs]
    # users = [x.user for x in rentItemLogs]
    # usersNames = [x.first_name for x in users]
    # usersLastNames = [x.last_name for x in users]
    # Students = Student.objects.filter(user_id=[x.id for x in users])
    #
    # roomsNumbers = Students
    # rentHour = [row.rentHour for row in rentItemLogs]
    # returnHour = [row.returnHour for row in rentItemLogs]
    # context = {
    #     'date' :dates,
    #     'date' :dates,
    #     'date' :dates,
    #     'date' :dates,
    #     'date' :dates,
    #     'date' :dates,
    #
    # }
    return render(request, "rental/rental.html")
