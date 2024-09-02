from functions.additional_functions import *
import decimal
from models import L_op, L_kredit

def po_invoice_btn_chgbl(s_list_s_recid:int):
    err_code = 0
    l_op = l_kredit = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, l_op, l_kredit


        return {"err_code": err_code}


    l_op = db_session.query(L_op).filter(
            (L_op._recid == s_list_s_recid)).first()

    l_kredit = db_session.query(L_kredit).filter(
            (L_kredit.lief_nr == l_op.lief_nr) &  (L_kredit.name == l_op.docu_nr) &  (L_kredit.lscheinnr == l_op.lscheinnr) &  (L_kredit.opart >= 1) &  (L_kredit.zahlkonto > 0)).first()

    if l_kredit:
        err_code = 1

        return generate_output()