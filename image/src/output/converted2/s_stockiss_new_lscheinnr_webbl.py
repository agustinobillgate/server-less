#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_ophdr

def s_stockiss_new_lscheinnr_webbl(lscheinnr:string, billdate:date, s:string):

    prepare_cache ([L_ophdr])

    i:int = 1
    l_ophdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, l_ophdr
        nonlocal lscheinnr, billdate, s

        return {"lscheinnr": lscheinnr}


    for l_ophdr in db_session.query(L_ophdr).filter(
             (L_ophdr.datum == billdate) & (L_ophdr.op_typ == ("STI").lower()) & (substring(L_ophdr.lscheinnr, 0, 7) == (s).lower())).order_by(L_ophdr.lscheinnr.desc()).all():
        lscheinnr = s + to_string(to_int(substring(l_ophdr.lscheinnr, 7, 3)) + 1, "999")
        break

    if not l_ophdr:
        lscheinnr = s + to_string(1, "999")

    return generate_output()