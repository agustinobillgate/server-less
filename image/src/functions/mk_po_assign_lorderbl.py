from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_orderhdr, L_order

def mk_po_assign_lorderbl(t_l_orderhdr:[T_l_orderhdr], lief_nr:int, docu_nr:str, pr:str, curr_liefnr:int):
    globaldisc:decimal = 0
    l_orderhdr = l_order = None

    t_l_orderhdr = None

    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal globaldisc, l_orderhdr, l_order


        nonlocal t_l_orderhdr
        nonlocal t_l_orderhdr_list
        return {}

    def assign_lorder():

        nonlocal globaldisc, l_orderhdr, l_order


        nonlocal t_l_orderhdr
        nonlocal t_l_orderhdr_list

        l_order = db_session.query(L_order).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.pos == 0) &  (L_order.loeschflag == 0) &  (L_order.lief_nr == curr_liefnr)).first()

        if l_order:
            l_order.lief_nr = lief_nr
            l_order.lief_fax[0] = pr
            l_order.warenwert = globaldisc

        for l_order in db_session.query(L_order).filter(
                (func.lower(L_order.(docu_nr).lower()) == (docu_nr).lower()) &  (L_order.loeschflag == 0) &  (L_order.lief_nr == curr_liefnr)).all():
            l_order.lief_nr = lief_nr
            l_order.betriebsnr = 0

        if curr_liefnr != lief_nr:
            l_orderhdr.lief_nr = lief_nr

        l_orderhdr = db_session.query(L_orderhdr).first()

    t_l_orderhdr = query(t_l_orderhdr_list, first=True)

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == t_L_orderhdr.rec_id)).first()

    if num_entries(t_l_orderhdr.lief_fax[2], chr(2)) > 1:
        globaldisc = decimal.Decimal(entry(1, t_l_orderhdr.lief_fax[2], chr(2))) / 100
        t_l_orderhdr.lief_fax[2] = entry(0, t_l_orderhdr.lief_fax[2], chr(2))


    buffer_copy(t_l_orderhdr, l_orderhdr)
    assign_lorder()

    return generate_output()