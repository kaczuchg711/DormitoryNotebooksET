def change_QuerySet_from_db_to_list(querySet, column_name):
    return [i[column_name] for i in [j for j in querySet]]

# def change_QuerySet_from_db_to_list(querySet,atribute):
#     entry_list = list(querySet)
#         for item in entry_list:
#             print(item.atribute)

def print_with_enters(*valuses):
    print("\n"*3)
    print(*valuses)
    print("\n"*3)