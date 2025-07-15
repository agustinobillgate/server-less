#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr

def mk_po_valchg_releaseflagbl(rec_id:int):

    prepare_cache ([L_orderhdr])

    l_orderhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr
        nonlocal rec_id

        return {}


    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id)]})
    pass
    l_orderhdr.gedruckt = get_current_date()
    pass

    return generate_output()