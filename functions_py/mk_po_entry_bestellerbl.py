#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import L_order

def mk_po_entry_bestellerbl(rec_id:int, bemerkung:string):

    prepare_cache ([L_order])

    l_order = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order
        nonlocal rec_id, bemerkung

        return {}


    # l_order = get_cache (L_order, {"_recid": [(eq, rec_id)]})
    l_order = db_session.query(L_order).filter(
                 (L_order._recid == rec_id)).with_for_update().first()
    l_order.besteller = bemerkung



    return generate_output()