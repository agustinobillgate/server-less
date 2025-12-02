#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr

def mk_pr_btn_stopbl(rec_id:int):
    l_orderhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr
        nonlocal rec_id

        return {}


    # l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id)]})
    l_orderhdr = db_session.query(L_orderhdr).filter(
                 (L_orderhdr._recid == rec_id)).with_for_update().first()
    db_session.delete(l_orderhdr)
    pass

    return generate_output()