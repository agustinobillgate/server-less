#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr, L_order

def mk_po_btn_stopbl(po_type:int, rec_id:int, lief_nr:int, docu_nr:string):
    l_orderhdr = l_order = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr, l_order
        nonlocal po_type, rec_id, lief_nr, docu_nr

        return {}


    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, rec_id)]})

    if po_type == 1:
        pass
        db_session.delete(l_orderhdr)

    for l_order in db_session.query(L_order).filter(
             (L_order.lief_nr == lief_nr) & (L_order.loeschflag == 0) & (L_order.pos >= 0) & (L_order.docu_nr == (docu_nr).lower()) & (L_order.betriebsnr == 2)).order_by(L_order._recid).all():
        db_session.delete(l_order)

    return generate_output()