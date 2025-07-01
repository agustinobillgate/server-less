#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr, Waehrung

def mk_po_btn_val_chg_currencybl(currency_screen_value:string, rec_id:int):

    prepare_cache ([L_orderhdr, Waehrung])

    int1 = 0
    l_orderhdr = waehrung = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal int1, l_orderhdr, waehrung
        nonlocal currency_screen_value, rec_id

        return {"int1": int1}


    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, currency_screen_value)]})
    l_orderhdr.angebot_lief[2] = waehrung.waehrungsnr
    pass
    int1 = l_orderhdr.angebot_lief[2]

    return generate_output()