from functions.additional_functions import *
import decimal
from models import L_orderhdr

def chg_po_btn_stopbl(case_type:int, rec_id_l_orderhdr:int, waehrung_waehrungsnr:int):
    l_orderhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr


        return {}


    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == rec_id_l_orderhdr)).first()

    if case_type == 1:

        l_orderhdr = db_session.query(L_orderhdr).first()
        l_orderhdr.gedruckt = None

        l_orderhdr = db_session.query(L_orderhdr).first()

    if case_type == 2:

        l_orderhdr = db_session.query(L_orderhdr).first()
        l_orderhdr.angebot_lief[2] = waehrung_waehrungsnr

        l_orderhdr = db_session.query(L_orderhdr).first()

    return generate_output()