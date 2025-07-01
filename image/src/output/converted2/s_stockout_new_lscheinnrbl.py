#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_ophdr

def s_stockout_new_lscheinnrbl(lscheinnr:string, rec_id:int, case_type:int, transdate:date, req_str:string, s:string):

    prepare_cache ([L_ophdr])

    i:int = 0
    j:int = 0
    l_ophdr = None

    l_ophdr1 = l_ophdr2 = None

    L_ophdr1 = create_buffer("L_ophdr1",L_ophdr)
    L_ophdr2 = create_buffer("L_ophdr2",L_ophdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, j, l_ophdr
        nonlocal lscheinnr, rec_id, case_type, transdate, req_str, s
        nonlocal l_ophdr1, l_ophdr2


        nonlocal l_ophdr1, l_ophdr2

        return {"lscheinnr": lscheinnr}


    l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, rec_id)]})

    if case_type == 1:

        l_ophdr1 = db_session.query(L_ophdr1).filter(
                 (substring(L_ophdr1.lscheinnr, 0, 3) == (lscheinnr).lower()) & (L_ophdr1.op_typ == ("STT").lower()) & (L_ophdr1.datum == transdate)).first()
        while None != l_ophdr1:
            i = i + 1
            lscheinnr = to_string(i, "999")

            l_ophdr1 = db_session.query(L_ophdr1).filter(
                     (substring(L_ophdr1.lscheinnr, 0, 3) == (lscheinnr).lower()) & (L_ophdr1.op_typ == ("STT").lower()) & (L_ophdr1.datum == transdate)).first()
        lscheinnr = lscheinnr + "-" + req_str
        pass
        l_ophdr.docu_nr = lscheinnr
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.op_typ = "STT"
        pass

    elif case_type == 2:

        l_ophdr1 = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "stt")]})
        while None != l_ophdr1:
            i = i + 1
            lscheinnr = s + to_string(i, "999")

            l_ophdr1 = get_cache (L_ophdr, {"lscheinnr": [(eq, lscheinnr)],"op_typ": [(eq, "stt")]})

        l_ophdr2 = db_session.query(L_ophdr2).filter(
                 (substring(L_ophdr2.lscheinnr, 0, 7) == (s).lower()) & (L_ophdr2.op_typ == ("STT").lower())).order_by(L_ophdr2._recid.desc()).first()

        if l_ophdr2:
            j = to_int(substring(l_ophdr2.lscheinnr, length(l_ophdr2.lscheinnr) - 2 - 1)) + 1

            if l_ophdr2._recid != l_ophdr1._recid:
                lscheinnr = s + to_string(j, "999")
        pass
        l_ophdr.docu_nr = lscheinnr
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.op_typ = "STT"
        pass

    return generate_output()