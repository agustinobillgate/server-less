from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_kredit

def dpchase_stockin_btn_pocancelbl(q2_list_lief_nr:int, q2_list_lscheinnr:str):
    avail_l_kredit = False
    l_kredit = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_kredit, l_kredit


        return {"avail_l_kredit": avail_l_kredit}


    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit.lief_nr == q2_list_lief_nr) &  (func.lower(L_kredit.name) == (q2_list_lscheinnr).lower()) &  (func.lower(L_kredit.lscheinnr) == (q2_list_lscheinnr).lower()) &  (L_kredit.zahlkonto > 0)).first()

    if l_kredit:
        avail_l_kredit = True

    return generate_output()