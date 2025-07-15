#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_lager

def s_stockins_leave_curr_lagerbl(curr_lager:int):

    prepare_cache ([L_lager])

    lager_bezeich = ""
    err_code = 0
    l_lager = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lager_bezeich, err_code, l_lager
        nonlocal curr_lager

        return {"lager_bezeich": lager_bezeich, "err_code": err_code}


    l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_lager)]})

    if l_lager:
        lager_bezeich = l_lager.bezeich
        err_code = 1

        return generate_output()

    return generate_output()