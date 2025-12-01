#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
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


    # l_order = get_cache (L_order, {"_recid": [(eq, t_recid)]})
    l_order = db_session.query(L_order).filter(
                 (L_order._recid == t_recid)).with_for_update().first()
    db_session.delete(l_order)

    return generate_output()