#using conversion tools version: 1.0.0.117

# ==============================================
# Rulita, 02-12-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def s_storerequest_new_lscheinnrbl(lscheinnr:string, s:string, recid_l_ophdr:int):
    i:int = 1
    l_ophdr = None

    l_ophdr1 = None

    L_ophdr1 = create_buffer("L_ophdr1",L_ophdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, l_ophdr
        nonlocal lscheinnr, s, recid_l_ophdr
        nonlocal l_ophdr1


        nonlocal l_ophdr1

        return {"lscheinnr": lscheinnr}


    # l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, recid_l_ophdr)]})
    l_ophdr = db_session.query(L_ophdr).filter(
             (L_ophdr._recid == recid_l_ophdr)).with_for_update().first()

    l_ophdr1 = db_session.query(L_ophdr1).filter(
             (L_ophdr1.lscheinnr == (lscheinnr).lower()) & (L_ophdr1.op_typ == ("REQ").lower())).first()
    while None != l_ophdr1:
        i = i + 1
        lscheinnr = s + to_string(i, "999")

        l_ophdr1 = db_session.query(L_ophdr1).filter(
                 (L_ophdr1.lscheinnr == (lscheinnr).lower()) & (L_ophdr1.op_typ == ("REQ").lower())).first()

    if l_ophdr:
        # pass
        l_ophdr.docu_nr = lscheinnr
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.op_typ = "REQ"
        # pass
        # pass
        db_session.refresh(l_ophdr, with_for_update=True)

    return generate_output()
