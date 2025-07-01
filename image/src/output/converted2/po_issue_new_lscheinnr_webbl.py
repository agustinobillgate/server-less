#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_ophdr

def po_issue_new_lscheinnr_webbl(billdate:date):

    prepare_cache ([L_ophdr])

    lscheinnr = ""
    l_ophdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lscheinnr, l_ophdr
        nonlocal billdate

        return {"lscheinnr": lscheinnr}

    def new_lscheinnr():

        nonlocal lscheinnr, l_ophdr
        nonlocal billdate

        s:string = ""
        i:int = 1
        s = "i" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")

        for l_ophdr in db_session.query(L_ophdr).filter(
                 (L_ophdr.datum == billdate) & (L_ophdr.op_typ == ("STI").lower()) & (substring(L_ophdr.lscheinnr, 0, 7) == (s).lower())).order_by(L_ophdr.lscheinnr.desc()).all():
            lscheinnr = s + to_string(to_int(substring(l_ophdr.lscheinnr, 7, 3)) + 1, "999")
            break

        if not l_ophdr:
            lscheinnr = s + to_string(1, "999")


    new_lscheinnr()

    return generate_output()