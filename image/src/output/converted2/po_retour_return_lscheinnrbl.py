#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def po_retour_return_lscheinnrbl(lscheinnr:string, docu_nr:string):
    err_code = 0
    l_ophdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, l_ophdr
        nonlocal lscheinnr, docu_nr

        return {"err_code": err_code}


    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "sti")],"docu_nr": [(eq, docu_nr)]})

    if not l_ophdr:
        err_code = 1

        return generate_output()

    return generate_output()