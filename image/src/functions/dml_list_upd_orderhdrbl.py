from functions.additional_functions import *
import decimal
from datetime import date
from models import L_orderhdr

def dml_list_upd_orderhdrbl(case_type:int, rec_id:int, dept:int, comments_screen_value:str, datum:date):
    l_orderhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr


        return {}


    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == rec_id)).first()

    if case_type == 1:

        l_orderhdr = db_session.query(L_orderhdr).first()
        l_orderhdr.angebot_lief[0] = dept

        l_orderhdr = db_session.query(L_orderhdr).first()

    elif case_type == 2:

        l_orderhdr = db_session.query(L_orderhdr).first()
        l_orderhdr.lief_fax[2] = comments_screen_value

        l_orderhdr = db_session.query(L_orderhdr).first()

    elif case_type == 3:

        l_orderhdr = db_session.query(L_orderhdr).first()
        l_orderhdr.lieferdatum = datum

        l_orderhdr = db_session.query(L_orderhdr).first()

    elif case_type == 4:

        l_orderhdr = db_session.query(L_orderhdr).first()
        db_session.delete(l_orderhdr)

    return generate_output()