from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_ophdr

def po_issue_new_lscheinnrbl(billdate:date):
    lscheinnr = ""
    l_ophdr = None

    l_ophdr1 = None

    L_ophdr1 = L_ophdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lscheinnr, l_ophdr
        nonlocal l_ophdr1


        nonlocal l_ophdr1
        return {"lscheinnr": lscheinnr}

    def new_lscheinnr():

        nonlocal lscheinnr, l_ophdr
        nonlocal l_ophdr1


        nonlocal l_ophdr1

        s:str = ""
        i:int = 1
        L_ophdr1 = L_ophdr
        s = "i" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")
        lscheinnr = s + to_string(i, "999")

        l_ophdr1 = db_session.query(L_ophdr1).filter(
                (L_ophdr1.datum == billdate) &  (func.lower(L_ophdr1.op_typ) == "STI") &  (substring(L_ophdr1.lscheinnr, 0, 10) == lscheinnr)).first()
        while None != l_ophdr1:
            i = i + 1
            lscheinnr = s + to_string(i, "999")

            l_ophdr1 = db_session.query(L_ophdr1).filter(
                    (L_ophdr1.datum == billdate) &  (func.lower(L_ophdr1.op_typ) == "STI") &  (substring(L_ophdr1.lscheinnr, 0, 10) == lscheinnr)).first()

    new_lscheinnr()

    return generate_output()