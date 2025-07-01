#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_op, L_order

def supply_inlist_update_it1bl(rec_id:int):

    prepare_cache ([L_op, L_order])

    l_op = l_order = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_op, l_order
        nonlocal rec_id

        return {}


    l_op = get_cache (L_op, {"_recid": [(eq, rec_id)]})

    for l_order in db_session.query(L_order).filter(
             (L_order.docu_nr == l_op.docu_nr) & (L_order.lief_nr == l_op.lief_nr) & (L_order.pos >= 0) & (L_order.loeschflag == 1)).order_by(L_order._recid).all():
        l_order.loeschflag = 0
        pass

    return generate_output()