#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import L_order, L_orderhdr

def mk_po_check_lief_nrbl(docu_nr:string, lief_nr:int):

    prepare_cache ([L_order, L_orderhdr])

    l_order = l_orderhdr = None

    db_session = local_storage.db_session
    docu_nr = docu_nr.strip().lower()

    def generate_output():
        nonlocal l_order, l_orderhdr
        nonlocal docu_nr, lief_nr

        return {}


    for l_order in db_session.query(L_order).filter(
             (L_order.docu_nr == (docu_nr).lower())).order_by(L_order._recid).with_for_update().all():
        l_order.lief_nr = lief_nr

    # l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)]})
    l_orderhdr = db_session.query(L_orderhdr).filter(
             (L_orderhdr.docu_nr == (docu_nr).lower())).with_for_update().first()   

    if l_orderhdr:
        l_orderhdr.lief_nr = lief_nr

    return generate_output()