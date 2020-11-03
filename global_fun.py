def change_QuerySet_from_db_to_list(querySet, column_name):
    return [i[column_name] for i in [j for j in querySet]]

def print_with_enters(string):
    print("\n"*5+string+"\n"*5)