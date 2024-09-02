from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_ophdr

def s_transform_new_lscheinnr1bl(lscheinnr:str, rec_id:int, transdate:date, req_str:str):
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
            (substring(L_ophdr1.(lscheinnr).lower() , 0, 3) == (lscheinnr).lower()) &  (func.lower(L_ophdr1.op_typ) == "STT") &  (L_ophdr1.datum == transdate)).first()
    while None != l_ophdr1:
        i = i + 1
        lscheinnr = to_string(i, "999")

        l_ophdr1 = db_session.query(L_ophdr1).filter(
                (substring(L_ophdr1.(lscheinnr).lower() , 0, 3) == (lscheinnr).lower()) &  (func.lower(L_ophdr1.op_typ) == "STT") &  (L_ophdr1.datum == transdate)).first()
    lscheinnr = lscheinnr + "-" + req_str

    l_ophdr = db_session.query(L_ophdr).filter(
            (L_ophdr._recid == rec_id)).first()

    l_ophdr = db_session.query(L_ophdr).first()
    l_ophdr.docu_nr = lscheinnr
    l_ophdr.lscheinnr = lscheinnr
    l_ophdr.op_typ = "STT"

    l_ophdr = db_session.query(L_ophdr).first()


    return generate_output()