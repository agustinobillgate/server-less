#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_orderhdr

def mk_po_btn_help_update_lorderhdrbl(case_type:int, rec_id:int, datum:date, dept:int):

    prepare_cache ([L_orderhdr])

    l_orderhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr
        nonlocal case_type, rec_id, datum, dept

        return {}


    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id)]})

    if case_type == 1:
        pass
        l_orderhdr.lieferdatum = datum

    elif case_type == 2:
        pass
        l_orderhdr.angebot_lief[0] = dept

    elif case_type == 3:
        pass
        l_orderhdr.gedruckt = get_current_date()
    pass

    return generate_output()