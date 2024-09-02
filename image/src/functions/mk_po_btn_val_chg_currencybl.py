from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_orderhdr, Waehrung

def mk_po_btn_val_chg_currencybl(currency_screen_value:str, rec_id:int):
    int1 = 0
    l_orderhdr = waehrung = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal int1, l_orderhdr, waehrung


        return {"int1": int1}


    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == rec_id)).first()

    waehrung = db_session.query(Waehrung).filter(
            (func.lower(Waehrung.wabkurz) == (currency_screen_value).lower())).first()
    l_orderhdr.angebot_lief[2] = waehrungsnr

    l_orderhdr = db_session.query(L_orderhdr).first()
    int1 = l_orderhdr.angebot_lief[2]

    return generate_output()