from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_order, L_orderhdr

def mk_po_btn_stop_webbl(po_type:int, rec_id:int, lief_nr:int, docu_nr:str):
    l_order = l_orderhdr = None

    l_od = None

    L_od = create_buffer("L_od",L_order)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order, l_orderhdr
        nonlocal po_type, rec_id, lief_nr, docu_nr
        nonlocal l_od


        nonlocal l_od
        return {}


    l_orderhdr = db_session.query(L_orderhdr).filter(
             (L_orderhdr._recid == rec_id)).first()

    if po_type == 1:
        db_session.refresh(l_orderhdr, with_for_update=True)
        db_session.delete(l_orderhdr)
        db_session.flush()

        for l_order in db_session.query(L_order).filter(
                 (L_order.lief_nr == lief_nr) & (L_order.loeschflag == 0) & (L_order.pos >= 0) & (func.lower(L_order.docu_nr) == (docu_nr).lower()) & (L_order.betriebsnr == 2)).with_for_update().order_by(L_order._recid).all():
            
            db_session.delete(l_order)

    elif po_type == 2:

        for l_order in db_session.query(L_order).filter(
                 (L_order.lief_nr == lief_nr) & (L_order.loeschflag == 0) & (L_order.pos >= 0) & (func.lower(L_order.docu_nr) == (docu_nr).lower()) & (L_order.betriebsnr >= 98)).order_by(L_order._recid).all():

            if l_order.betriebsnr == 98:

                l_od = db_session.query(L_od).filter(
                         (L_od._recid == l_order._recid)).with_for_update().first()
                db_session.delete(l_od)

            if l_order.betriebsnr == 99:

                l_od = db_session.query(L_od).filter(
                         (L_od._recid == l_order._recid)).with_for_update().first()
                
                l_od.betriebsnr = 2
                l_od.anzahl =  to_decimal(l_od.anzahl) - to_decimal(l_od.geliefert)
                l_od.geliefert =  to_decimal("0")
                l_od.warenwert =  to_decimal(l_od.anzahl) * to_decimal(l_od.einzelpreis)

    return generate_output()