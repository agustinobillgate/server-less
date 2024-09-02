from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_orderhdr, L_order

def mk_po_btn_stopbl(po_type:int, rec_id:int, lief_nr:int, docu_nr:str):
    l_orderhdr = l_order = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr, l_order


        return {}


    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == rec_id)).first()

    if po_type == 1:

        l_orderhdr = db_session.query(L_orderhdr).first()
        db_session.delete(l_orderhdr)

    for l_order in db_session.query(L_order).filter(
            (L_order.lief_nr == lief_nr) &  (L_order.loeschflag == 0) &  (L_order.pos >= 0) &  (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.betriebsnr == 2)).all():
        db_session.delete(l_order)

    return generate_output()