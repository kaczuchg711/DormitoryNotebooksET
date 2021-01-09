import time as basic_time
from django.core.handlers.wsgi import WSGIRequest


def change_QuerySet_from_db_to_list(querySet, column_name):
    querySet = querySet.values(column_name)
    return [i[column_name] for i in [j for j in querySet]]


# def change_QuerySet_from_db_to_list(querySet,atribute):
#     entry_list = list(querySet)
#         for item in entry_list:
#             print(item.atribute)

def print_with_enters(*valuses):
    print("\n" * 3)
    print(*valuses)
    print("\n" * 3)


def get_actual_time():
    t = basic_time.localtime()
    actual_time = basic_time.strftime("%H:%M:%S", t)
    return actual_time

def print_Post(request: WSGIRequest):
    print("POST:")
    for i in request.POST:
        print('{:>30} => {}'.format(i,request.POST[i]))

def print_session(request: WSGIRequest):
    print("session:")
    for key, value in request.session.items():
        print('{:>30} => {}'.format(key, value))

def make_unique_list(collection):
    collection = set(collection)
    return list(collection)
