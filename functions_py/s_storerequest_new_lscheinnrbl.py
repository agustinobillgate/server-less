# using conversion tools version: 1.0.0.117

# ==============================================
# Rulita, 02-12-2025
# - Added with_for_update all query

# yusufwijasena_29/12/2025
# fix lscheinnr duplication issue
# fix update lscheinnr to database
# fix validation for l_ophdr1
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr


def s_storerequest_new_lscheinnrbl(lscheinnr: string, s: string, recid_l_ophdr: int):
    i: int = 1
    l_ophdr = None

    l_ophdr1 = None

    L_ophdr1 = create_buffer("L_ophdr1", L_ophdr)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, l_ophdr
        nonlocal lscheinnr, s, recid_l_ophdr
        nonlocal l_ophdr1

        return {
            "lscheinnr": lscheinnr
        }

    # l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, recid_l_ophdr)]})   
    # check l_ophdr by _recid number
    l_ophdr = db_session.query(L_ophdr).filter(
        (L_ophdr._recid == recid_l_ophdr)).first()    
    
    # print("[LOG] l_ophdr by _recid", l_ophdr._recid if l_ophdr else "Not Found")

    # check l_ophdr by lscheinnr
    l_ophdr1 = db_session.query(L_ophdr1).filter(
        (func.lower(L_ophdr1.lscheinnr) == (lscheinnr).lower()) &
        (func.lower(L_ophdr1.op_typ) == "req")).first()
    
    # print("[LOG] l_ophdr1 by lscheinnr", l_ophdr1._recid if l_ophdr1 else "Not Found")
    while l_ophdr1:
        i = i + 1
        lscheinnr = s + to_string(i, "999")
        
        l_ophdr1 = db_session.query(L_ophdr1).filter(
            (func.lower(L_ophdr1.lscheinnr) == (lscheinnr).lower()) &
            (func.lower(L_ophdr1.op_typ) == "req")).with_for_update().first()

    # if lscheinnr not found then updated to l_ophdr with same recid
    if l_ophdr:
        l_ophdr.docu_nr = lscheinnr
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.op_typ = "req"
        
        db_session.commit()

        # db_session.refresh(l_ophdr, with_for_update=True)

    return generate_output()
