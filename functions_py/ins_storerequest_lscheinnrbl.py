#using conversion tools version: 1.0.0.117

# ==============================================
# Rulita, 02-12-2025
# - Added with_for_update all query 
# =============================================

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


    # l_ophdr = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "req")]})
    l_ophdr = db_session.query(L_ophdr).filter(
             (L_ophdr.lscheinnr == lscheinnr) & (L_ophdr.op_typ == "req")).with_for_update().first()

    if casetype == 1:
        # pass
        l_ophdr.docu_nr = lscheinnr
        l_ophdr.lscheinnr = lscheinnr
        # pass
        db_session.refresh(l_ophdr, with_for_update=True)

    elif casetype == 2:

        if l_ophdr:
            err = 1

            return generate_output()

    return generate_output()
