#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Mc_types, Mc_guest, Mc_fee

def mc_gcf0_readbl(case_type:int, int1:int):

    prepare_cache ([Mc_guest, Mc_fee])

    flag = False
    mc_types = mc_guest = mc_fee = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, mc_types, mc_guest, mc_fee
        nonlocal case_type, int1

        return {"flag": flag}


    if case_type == 1:

        mc_types = get_cache (Mc_types, {"nr": [(eq, int1)]})

        if mc_types:
            flag = True

    elif case_type == 2:

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, int1)]})

        mc_fee = get_cache (Mc_fee, {"key": [(eq, 1)],"gastnr": [(eq, mc_guest.gastnr)],"bis_datum": [(eq, mc_guest.tdate)]})

        if mc_fee and mc_fee.bezahlt != 0:
            flag = True

    return generate_output()