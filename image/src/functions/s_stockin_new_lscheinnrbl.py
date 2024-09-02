from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_ophdr

def s_stockin_new_lscheinnrbl(lscheinnr:str, billdate:date, s:str):
    i:int = 1
    l_ophdr = None

    l_ophdr1 = None

    L_ophdr1 = L_ophdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, l_ophdr
        nonlocal l_ophdr1


        nonlocal l_ophdr1
        return {}


    l_ophdr1 = db_session.query(L_ophdr1).filter(
            (L_ophdr1.datum == billdate) &  (func.lower(L_ophdr1.op_typ) == "STI") &  (substring(L_ophdr1.(lscheinnr).lower() , 0, 10) == (lscheinnr).lower())).first()
    while None != l_ophdr1:
        i = i + 1
        lscheinnr = s + to_string(i, "999")

        l_ophdr1 = db_session.query(L_ophdr1).filter(
                (L_ophdr1.datum == billdate) &  (func.lower(L_ophdr1.op_typ) == "STI") &  (substring(L_ophdr1.(lscheinnr).lower() , 0, 10) == (lscheinnr).lower())).first()

    return generate_output()