#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr

def chg_po_btn_stopbl(case_type:int, rec_id_l_orderhdr:int, waehrung_waehrungsnr:int):

    prepare_cache ([L_orderhdr])

    l_orderhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr
        nonlocal case_type, rec_id_l_orderhdr, waehrung_waehrungsnr

        return {}


    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id_l_orderhdr)]})

    if case_type == 1:
        pass
        l_orderhdr.gedruckt = None


        pass

    if case_type == 2:
        pass
        l_orderhdr.angebot_lief[2] = waehrung_waehrungsnr


        pass

    return generate_output()