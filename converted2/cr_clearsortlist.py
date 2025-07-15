from functions.additional_functions import *
import decimal
from datetime import date

def cr_clearsortlist():


    temp_table = None

    temp_table_list, Temp_table = create_model("Temp_table", {"selected":bool, "gastnr":int, "guestname":str, "address":str, "karteityp":int, "guest_type":str, "birthday":date, "city":str, "land1":str, "nation":str, "gender":str, "mphone":str, "email":str}, {"selected": True})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_table
        nonlocal temp_table_list

        return {}


    sort_list_list.clear()

    return generate_output()