#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def s_stockout_return_lscheinnrbl(lscheinnr:string):
    avail_l_ophdr = False
    l_ophdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_ophdr, l_ophdr
        nonlocal lscheinnr

        return {"avail_l_ophdr": avail_l_ophdr}


    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "stt")]})

    if l_ophdr:
        avail_l_ophdr = True

    return generate_output()