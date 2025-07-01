#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_ophdr

def po_issue_new_lscheinnrbl(billdate:date):
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

        l_ophdr1 = None
        s:string = ""
        i:int = 1
        L_ophdr1 =  create_buffer("L_ophdr1",L_ophdr)
        s = "i" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")
        lscheinnr = s + to_string(i, "999")

        l_ophdr1 = db_session.query(L_ophdr1).filter(
                 (L_ophdr1.datum == billdate) & (L_ophdr1.op_typ == ("STI").lower()) & (substring(L_ophdr1.lscheinnr, 0, 10) == (lscheinnr).lower())).first()
        while None != l_ophdr1:
            i = i + 1
            lscheinnr = s + to_string(i, "999")

            l_ophdr1 = db_session.query(L_ophdr1).filter(
                     (L_ophdr1.datum == billdate) & (L_ophdr1.op_typ == ("STI").lower()) & (substring(L_ophdr1.lscheinnr, 0, 10) == (lscheinnr).lower())).first()


    new_lscheinnr()

    return generate_output()