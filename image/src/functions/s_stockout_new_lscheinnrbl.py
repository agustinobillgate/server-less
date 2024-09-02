from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_ophdr

def s_stockout_new_lscheinnrbl(lscheinnr:str, rec_id:int, case_type:int, transdate:date, req_str:str, s:str):
    i:int = 0
    j:int = 0
    l_ophdr = None

    l_ophdr1 = l_ophdr2 = None

    L_ophdr1 = L_ophdr
    L_ophdr2 = L_ophdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, j, l_ophdr
        nonlocal l_ophdr1, l_ophdr2


        nonlocal l_ophdr1, l_ophdr2
        return {}


    l_ophdr = db_session.query(L_ophdr).filter(
            (L_ophdr._recid == rec_id)).first()

    if case_type == 1:

        l_ophdr1 = db_session.query(L_ophdr1).filter(
                (substring(L_ophdr1.(lscheinnr).lower() , 0, 3) == (lscheinnr).lower()) &  (func.lower(L_ophdr1.op_typ) == "STT") &  (L_ophdr1.datum == transdate)).first()
        while None != l_ophdr1:
            i = i + 1
            lscheinnr = to_string(i, "999")

            l_ophdr1 = db_session.query(L_ophdr1).filter(
                    (substring(L_ophdr1.(lscheinnr).lower() , 0, 3) == (lscheinnr).lower()) &  (func.lower(L_ophdr1.op_typ) == "STT") &  (L_ophdr1.datum == transdate)).first()
        lscheinnr = lscheinnr + "-" + req_str

        l_ophdr = db_session.query(L_ophdr).first()
        l_ophdr.docu_nr = lscheinnr
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.op_typ = "STT"

        l_ophdr = db_session.query(L_ophdr).first()


    elif case_type == 2:

        l_ophdr1 = db_session.query(L_ophdr1).filter(
                (func.lower(L_ophdr1.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr1.op_typ) == "STT")).first()
        while None != l_ophdr1:
            i = i + 1
            lscheinnr = s + to_string(i, "999")

            l_ophdr1 = db_session.query(L_ophdr1).filter(
                    (func.lower(L_ophdr1.(lscheinnr).lower()) == (lscheinnr).lower()) &  (func.lower(L_ophdr1.op_typ) == "STT")).first()

        l_ophdr2 = db_session.query(L_ophdr2).filter(
                (substring(L_ophdr2.lscheinnr, 0, 7) == (s).lower()) &  (func.lower(L_ophdr2.op_typ) == "STT")).first()

        if l_ophdr2:
            j = to_int(substring(l_ophdr2.lscheinnr, len(l_ophdr2.lscheinnr) - 2 - 1)) + 1

            if l_ophdr2._recid != l_ophdr1._recid:
                lscheinnr = s + to_string(j, "999")

        l_ophdr = db_session.query(L_ophdr).first()
        l_ophdr.docu_nr = lscheinnr
        l_ophdr.lscheinnr = lscheinnr
        l_ophdr.op_typ = "STT"

        l_ophdr = db_session.query(L_ophdr).first()


    return generate_output()