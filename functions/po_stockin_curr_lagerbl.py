#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_lager

def po_stockin_curr_lagerbl(curr_lager:int):

    prepare_cache ([L_lager])

    avail_l_lager = False
    l_lager_bezeich = ""
    l_lager = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_lager, l_lager_bezeich, l_lager
        nonlocal curr_lager

        return {"avail_l_lager": avail_l_lager, "l_lager_bezeich": l_lager_bezeich}


    l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_lager)]})

    if l_lager:
        l_lager_bezeich = l_lager.bezeich
        avail_l_lager = True

    return generate_output()