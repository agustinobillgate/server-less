from functions.additional_functions import *
import decimal
from datetime import date
from models import L_orderhdr

def mk_po_btn_help_update_lorderhdrbl(case_type:int, rec_id:int, datum:date, dept:int):
    l_orderhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr


        return {}


    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == rec_id)).first()

    if case_type == 1:

        l_orderhdr = db_session.query(L_orderhdr).first()
        l_orderhdr.lieferdatum = datum

    elif case_type == 2:

        l_orderhdr = db_session.query(L_orderhdr).first()
        l_orderhdr.angebot_lief[0] = dept

    elif case_type == 3:

        l_orderhdr = db_session.query(L_orderhdr).first()
        l_orderhdr.gedruckt = get_current_date()

    l_orderhdr = db_session.query(L_orderhdr).first()

    return generate_output()