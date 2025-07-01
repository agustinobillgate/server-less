#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_order

def ins_pr_btn_delbl(t_recid:int):
    l_order = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order
        nonlocal t_recid

        return {}


    l_order = get_cache (L_order, {"_recid": [(eq, t_recid)]})
    pass
    db_session.delete(l_order)
    pass

    return generate_output()