from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import views as auth_views

from global_fun import print_with_enters, print_session, change_QuerySet_from_db_to_list, make_unique_list
from rental.models.DBmodels.Item import Item


@login_required(redirect_field_name='', login_url='/')
def get_choice_view(request):
    # todo get items which are available in dorm
    # dorm_id = request.
    dorm_id = request.session["dorm_id"]
    itemsInDorm = Item.objects.filter(dorm_id=dorm_id).values_list("name")
    itemsInDorm = make_unique_list(itemsInDorm)
    itemsInDorm = _unpack_from_tuples(itemsInDorm)

    context = {
        "itemsInDorm": itemsInDorm
    }

    return render(request, "panel/choice.html", context=context)


def _unpack_from_tuples(list):
    return [tuple[0] for tuple in list]
