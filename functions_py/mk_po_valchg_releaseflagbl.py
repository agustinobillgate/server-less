#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr
from sqlalchemy.orm import flag_modified
def mk_po_valchg_releaseflagbl(rec_id:int):

    prepare_cache ([L_orderhdr])

    l_orderhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr
        nonlocal rec_id

        return {}


    # l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id)]})
    l_orderhdr = db_session.query(L_orderhdr).filter(
                 (L_orderhdr._recid == rec_id)).with_for_update().first()
    l_orderhdr.gedruckt = get_current_date()

    return generate_output()