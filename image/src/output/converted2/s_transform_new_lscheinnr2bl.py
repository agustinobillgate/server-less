#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_ophdr

def s_transform_new_lscheinnr2bl(lscheinnr:string, rec_id:int, transdate:date, req_str:string, s:string):
    i:int = 1
    l_ophdr = None

    l_ophdr1 = None

    L_ophdr1 = create_buffer("L_ophdr1",L_ophdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, l_ophdr
        nonlocal lscheinnr, rec_id, transdate, req_str, s
        nonlocal l_ophdr1


        nonlocal l_ophdr1

        return {"lscheinnr": lscheinnr}


    l_ophdr1 = db_session.query(L_ophdr1).filter(
             (L_ophdr1.lscheinnr == (lscheinnr).lower()) & (L_ophdr1.op_typ == ("STT").lower())).first()
    while None != l_ophdr1:
        i = i + 1
        lscheinnr = s + to_string(i, "999")

        l_ophdr1 = db_session.query(L_ophdr1).filter(
                 (L_ophdr1.lscheinnr == (lscheinnr).lower()) & (L_ophdr1.op_typ == ("STT").lower())).first()

    l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, rec_id)]})
    pass
    l_ophdr.docu_nr = lscheinnr
    l_ophdr.lscheinnr = lscheinnr
    l_ophdr.op_typ = "STT"
    pass

    return generate_output()