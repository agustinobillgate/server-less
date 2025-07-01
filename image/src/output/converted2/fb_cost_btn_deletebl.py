#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def fb_cost_btn_deletebl(price_list_artnr:int):

    prepare_cache ([Queasy])

    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal price_list_artnr

        return {}


    queasy = get_cache (Queasy, {"key": [(eq, 142)],"number1": [(eq, price_list_artnr)]})

    if queasy:
        pass
        queasy.number1 = 0
        queasy.number2 = 0
        queasy.deci1 =  to_decimal("0")
        queasy.deci2 =  to_decimal("0")
        queasy.date1 = None
        queasy.date2 = None
        queasy.char2 = ""


        pass
        pass

    return generate_output()