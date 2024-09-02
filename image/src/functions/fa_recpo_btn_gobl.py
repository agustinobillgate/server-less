from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Fa_op, Fa_order, Fa_ordheader

def fa_recpo_btn_gobl(op_list:[Op_list], docu_nr:str, billdate:date, user_init:str, supplier_nr:int, supp_name:str, del_note:str, order_nr:str):
    allowclose = False
    art_nr:int = 0
    qty:int = 0
    price:decimal = 0
    amount:decimal = 0
    t_amount:decimal = 0
    fa_op = fa_order = fa_ordheader = None

    op_list = None

    op_list_list, Op_list = create_model_like(Fa_op, {"counter":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal allowclose, art_nr, qty, price, amount, t_amount, fa_op, fa_order, fa_ordheader


        nonlocal op_list
        nonlocal op_list_list
        return {"allowclose": allowclose}

    def close_po():

        nonlocal allowclose, art_nr, qty, price, amount, t_amount, fa_op, fa_order, fa_ordheader


        nonlocal op_list
        nonlocal op_list_list

        for fa_order in db_session.query(Fa_order).filter(
                (func.lower(Fa_order.(order_nr).lower()) == (order_nr).lower())).all():

            if allowclose :

                if fa_order.order_qty == fa_order.delivered_qty:
                    allowclose = True
                else:
                    allowclose = False
            else:
                allowclose = False

        if allowclose :

            fa_ordheader = db_session.query(Fa_ordheader).filter(
                    (func.lower(Fa_ordheader.(order_nr).lower()) == (order_nr).lower())).first()

            if fa_ordheader:
                fa_ordheader.activeflag = 1
                fa_ordheader.close_by = user_init
                fa_ordheader.close_date = billdate
                fa_ordheader.close_time = get_current_time_in_seconds()

            fa_ordheader = db_session.query(Fa_ordheader).first()


    close_po()

    return generate_output()