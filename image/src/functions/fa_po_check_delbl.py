from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Fa_order

def fa_po_check_delbl(q_order_nr:str):
    found = False
    fa_order = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal found, fa_order


        return {"found": found}


    fa_order = db_session.query(Fa_order).filter(
            (func.lower(Fa_order.order_nr) == (q_order_nr).lower()) &  (Fa_order.fa_pos > 0) &  (Fa_order.activeflag == 0) &  ((Fa_order.order_qty != Fa_order.delivered_qty))).first()

    if fa_order:
        found = True
    else:
        while (not found) and fa_order:

            fa_order = db_session.query(Fa_order).filter(
                    (func.lower(Fa_order.order_nr) == (q_order_nr).lower()) &  (Fa_order.fa_pos > 0) &  (Fa_order.activeflag == 0) &  ((Fa_order.order_qty != Fa_order.delivered_qty))).first()

            if fa_order:
                found = True

    return generate_output()