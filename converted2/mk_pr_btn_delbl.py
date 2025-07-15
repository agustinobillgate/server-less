#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_order

def mk_pr_btn_delbl(rec_id:int):
    l_order = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order
        nonlocal rec_id

        return {}


    l_order = get_cache (L_order, {"_recid": [(eq, rec_id)]})

    if l_order:
        pass
        db_session.delete(l_order)
        pass

    return generate_output()