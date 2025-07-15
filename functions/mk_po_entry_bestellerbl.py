#using conversion tools version: 1.0.0.117

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


    l_order = get_cache (L_order, {"_recid": [(eq, rec_id)]})
    pass
    l_order.besteller = bemerkung


    pass

    return generate_output()