#using conversion tools version: 1.0.0.117

# ==============================================
# Rulita, 02-12-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def supply_inlist_leave_invoice_nr_webbl(h_recid:int, invoice_nr:string):

    prepare_cache ([L_ophdr])

    l_ophdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_ophdr
        nonlocal h_recid, invoice_nr

        return {}


    # l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, h_recid)]})
    l_ophdr = db_session.query(L_ophdr).filter(
             (L_ophdr._recid == h_recid)).with_for_update().first()

    if l_ophdr:
        l_ophdr.fibukonto = trim(invoice_nr)
        pass

    return generate_output()
