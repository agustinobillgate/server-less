#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_order

def fa_po_check_delbl(q_order_nr:string):

    prepare_cache ([Fa_order])

    found = False
    fa_order = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal found, fa_order
        nonlocal q_order_nr

        return {"found": found}


    fa_order = get_cache (Fa_order, {"order_nr": [(eq, q_order_nr)],"fa_pos": [(gt, 0)],"activeflag": [(eq, 0)],"order_qty": [(ne, Fa_order.delivered_qty)]})

    if fa_order:
        found = True
    else:
        while (not found) and fa_order:

            curr_recid = fa_order._recid
            fa_order = db_session.query(Fa_order).filter(
                     (Fa_order.order_nr == (q_order_nr).lower()) & (Fa_order.fa_pos > 0) & (Fa_order.activeflag == 0) & ((Fa_order.order_qty != Fa_order.delivered_qty)) & (Fa_order._recid > curr_recid)).first()

            if fa_order:
                found = True

    return generate_output()