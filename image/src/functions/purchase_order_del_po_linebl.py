from functions.additional_functions import *
import decimal
from datetime import date
from models import L_order, L_orderhdr

def purchase_order_del_po_linebl(billdate:date, rec_id:int, l_orderhdr_rec_id:int, bediener_username:str):
    del_mainpo = False
    l_order = l_orderhdr = None

    l_od = None

    L_od = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal del_mainpo, l_order, l_orderhdr
        nonlocal l_od


        nonlocal l_od
        return {"del_mainpo": del_mainpo}

    def del_po_line():

        nonlocal del_mainpo, l_order, l_orderhdr
        nonlocal l_od


        nonlocal l_od


        L_od = L_order

        l_order = db_session.query(L_order).first()
        l_order.loeschflag = 2
        l_order.lieferdatum = billdate
        l_order.lief_fax[1] = bediener_username

        l_order = db_session.query(L_order).first()

        l_od = db_session.query(L_od).filter(
                (L_od.docu_nr == l_orderhdr.docu_nr) &  (L_od.pos > 0) &  (L_od.loeschflag == 0)).first()

        if not l_od:

            l_od = db_session.query(L_od).filter(
                    (L_od.docu_nr == l_orderhdr.docu_nr) &  (L_od.pos == 0)).first()
            l_od.loeschflag = 2
            l_od.lieferdatum_eff = billdate
            l_od.lief_fax[2] = bediener_username

            l_od = db_session.query(L_od).first()
        del_mainpo = True


    l_order = db_session.query(L_order).filter(
            (L_order._recid == rec_id)).first()

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == l_orderhdr_rec_id)).first()
    del_po_line()

    return generate_output()