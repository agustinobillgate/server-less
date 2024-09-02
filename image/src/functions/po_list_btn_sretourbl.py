from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_kredit

def po_list_btn_sretourbl(l_orderhdr_lief_nr:int, l_orderhdr_docu_nr:str):
    avail_l_kredit = False
    l_kredit = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_l_kredit, l_kredit


        return {"avail_l_kredit": avail_l_kredit}


    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit.lief_nr == l_orderhdr_lief_nr) &  (func.lower(L_kredit.name) == (l_orderhdr_docu_nr).lower()) &  (L_kredit.zahlkonto > 0)).first()

    if l_kredit:
        avail_l_kredit = True

    return generate_output()