#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_ophdr

def s_stockiss_new_lscheinnrbl(lscheinnr:string, billdate:date, s:string):
    i:int = 1
    l_ophdr = None

    l_ophdr1 = None

    L_ophdr1 = create_buffer("L_ophdr1",L_ophdr)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, l_ophdr
        nonlocal lscheinnr, billdate, s
        nonlocal l_ophdr1


        nonlocal l_ophdr1

        return {"lscheinnr": lscheinnr}


    l_ophdr1 = db_session.query(L_ophdr1).filter(
             (L_ophdr1.datum == billdate) & (L_ophdr1.op_typ == ("STI").lower()) & (substring(L_ophdr1.lscheinnr, 0, 10) == (lscheinnr).lower())).first()
    while None != l_ophdr1:
        i = i + 1
        lscheinnr = s + to_string(i, "999")

        l_ophdr1 = db_session.query(L_ophdr1).filter(
                 (L_ophdr1.datum == billdate) & (L_ophdr1.op_typ == ("STI").lower()) & (substring(L_ophdr1.lscheinnr, 0, 10) == (lscheinnr).lower())).first()

    return generate_output()