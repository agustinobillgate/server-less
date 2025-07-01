#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lager

def ins_storerequest_to_stockbl(to_stock:int, curr_lager:int):

    prepare_cache ([L_lager])

    lager_bez1 = ""
    flag = 0
    l_lager = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lager_bez1, flag, l_lager
        nonlocal to_stock, curr_lager

        return {"lager_bez1": lager_bez1, "flag": flag}


    l_lager = get_cache (L_lager, {"lager_nr": [(eq, to_stock)]})

    if not l_lager:
        flag = 1

        return generate_output()

    if to_stock == curr_lager:
        flag = 2

        return generate_output()
    lager_bez1 = l_lager.bezeich

    return generate_output()