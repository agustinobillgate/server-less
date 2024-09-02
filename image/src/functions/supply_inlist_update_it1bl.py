from functions.additional_functions import *
import decimal
from models import L_op, L_order

def supply_inlist_update_it1bl(rec_id:int):
    l_op = l_order = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_op, l_order


        return {}


    l_op = db_session.query(L_op).filter(
            (L_op._recid == rec_id)).first()

    for l_order in db_session.query(L_order).filter(
            (L_order.docu_nr == l_op.docu_nr) &  (L_order.lief_nr == l_op.lief_nr) &  (L_order.pos >= 0) &  (L_order.loeschflag == 1)).all():
        l_order.loeschflag = 0


    return generate_output()