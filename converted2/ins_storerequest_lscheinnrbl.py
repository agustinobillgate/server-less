#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def ins_storerequest_lscheinnrbl(casetype:int, lscheinnr:string):

    prepare_cache ([L_ophdr])

    err = 0
    l_ophdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, l_ophdr
        nonlocal casetype, lscheinnr

        return {"err": err}


    l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "req")]})

    if casetype == 1:
        pass
        l_ophdr.docu_nr = lscheinnr
        l_ophdr.lscheinnr = lscheinnr
        pass

    elif casetype == 2:

        if l_ophdr:
            err = 1

            return generate_output()

    return generate_output()