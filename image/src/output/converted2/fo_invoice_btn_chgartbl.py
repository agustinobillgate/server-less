#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt

def fo_invoice_btn_chgartbl(new_dept:int):

    prepare_cache ([Hoteldpt])

    hotel_depart = ""
    hoteldpt = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal hotel_depart, hoteldpt
        nonlocal new_dept

        return {"hotel_depart": hotel_depart}


    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, new_dept)]})
    hotel_depart = hoteldpt.depart

    return generate_output()