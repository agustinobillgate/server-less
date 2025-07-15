#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_order, Fa_ordheader

s_order_data, S_order = create_model_like(Fa_order)

def fa_chgpo_save_detailbl(s_order_data:[S_order], order_nr:string, credit_term:int, curr:int, dept_nr:int, order_date:date, supplier_nr:int, expected_delivery:date, order_type:string, order_name:string, comments:string, user_init:string, billdate:date, appr_1:bool):

    prepare_cache ([Fa_ordheader])

    pos:int = 0
    total_order:Decimal = to_decimal("0.0")
    fa_order = fa_ordheader = None

    s_order = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pos, total_order, fa_order, fa_ordheader
        nonlocal order_nr, credit_term, curr, dept_nr, order_date, supplier_nr, expected_delivery, order_type, order_name, comments, user_init, billdate, appr_1


        nonlocal s_order

        return {}

    fa_ordheader = get_cache (Fa_ordheader, {"order_nr": [(eq, order_nr)]})

    if fa_ordheader:
        fa_ordheader.order_nr = order_nr
        fa_ordheader.credit_term = credit_term
        fa_ordheader.currency = curr
        fa_ordheader.dept_nr = dept_nr
        fa_ordheader.order_date = order_date
        fa_ordheader.supplier_nr = supplier_nr
        fa_ordheader.expected_delivery = expected_delivery
        fa_ordheader.order_type = order_type
        fa_ordheader.order_name = order_name
        fa_ordheader.order_desc = comments
        fa_ordheader.modified_by = user_init
        fa_ordheader.modified_date = billdate
        fa_ordheader.modified_time = get_current_time_in_seconds()

        if fa_ordheader.approved_1 == False and appr_1 :
            fa_ordheader.approved_1 = appr_1
            fa_ordheader.approved_1_by = user_init
            fa_ordheader.approved_1_date = billdate
            fa_ordheader.approved_1_time = get_current_time_in_seconds()
            fa_ordheader.approved_2 = appr_1
            fa_ordheader.approved_2_by = user_init
            fa_ordheader.approved_2_date = billdate
            fa_ordheader.approved_2_time = get_current_time_in_seconds()
            fa_ordheader.approved_3 = appr_1
            fa_ordheader.approved_3_by = user_init
            fa_ordheader.approved_3_date = billdate
            fa_ordheader.approved_3_time = get_current_time_in_seconds()

        if fa_ordheader.released_flag == False:

            if fa_ordheader.approved_1 :
                fa_ordheader.released_flag = True
                fa_ordheader.released_date = billdate
                fa_ordheader.released_time = get_current_time_in_seconds()

    for fa_order in db_session.query(Fa_order).filter(
             (Fa_order.order_nr == (order_nr).lower())).order_by(Fa_order._recid).all():
        db_session.delete(fa_order)

    for s_order in query(s_order_data):
        pos = pos + 1
        total_order =  to_decimal(total_order) + to_decimal(s_order.order_amount)
        fa_order = Fa_order()
        db_session.add(fa_order)

        fa_order.order_nr = s_order.order_nr
        fa_order.fa_nr = s_order.fa_nr
        fa_order.order_qty = s_order.order_qty
        fa_order.order_price =  to_decimal(s_order.order_price)
        fa_order.discount1 =  to_decimal(s_order.discount1)
        fa_order.discount2 =  to_decimal(s_order.discount2)
        fa_order.vat =  to_decimal(s_order.vat)
        fa_order.order_amount =  to_decimal(s_order.order_amount)
        fa_order.fa_remarks = s_order.fa_remarks
        fa_order.statflag = 0
        fa_order.fa_pos = pos
        fa_order.op_art = 2
        fa_order.last_id = user_init


    fa_ordheader.total_amount =  to_decimal(total_order)

    return generate_output()