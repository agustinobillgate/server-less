#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def get_vipnrbl():

    prepare_cache ([Htparam])

    vipnr1 = 999999999
    vipnr2 = 999999999
    vipnr3 = 999999999
    vipnr4 = 999999999
    vipnr5 = 999999999
    vipnr6 = 999999999
    vipnr7 = 999999999
    vipnr8 = 999999999
    vipnr9 = 999999999
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, htparam

        return {"vipnr1": vipnr1, "vipnr2": vipnr2, "vipnr3": vipnr3, "vipnr4": vipnr4, "vipnr5": vipnr5, "vipnr6": vipnr6, "vipnr7": vipnr7, "vipnr8": vipnr8, "vipnr9": vipnr9}

    def get_vipnr():

        nonlocal vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, htparam

        htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

        if htparam.finteger != 0:
            vipnr1 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

        if htparam.finteger != 0:
            vipnr2 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

        if htparam.finteger != 0:
            vipnr3 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

        if htparam.finteger != 0:
            vipnr4 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

        if htparam.finteger != 0:
            vipnr5 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

        if htparam.finteger != 0:
            vipnr6 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

        if htparam.finteger != 0:
            vipnr7 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

        if htparam.finteger != 0:
            vipnr8 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

        if htparam.finteger != 0:
            vipnr9 = htparam.finteger


    get_vipnr()

    return generate_output()