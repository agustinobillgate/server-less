from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Fa_order, Fa_ordheader

def fa_chgpo_save_detailbl(s_order:[S_order], order_nr:str, credit_term:int, curr:int, dept_nr:int, order_date:date, supplier_nr:int, expected_delivery:date, order_type:str, order_name:str, comments:str, user_init:str, billdate:date, appr_1:bool):
    pos:int = 0
    total_order:decimal = 0
    fa_order = fa_ordheader = None

    s_order = None

    s_order_list, S_order = create_model_like(Fa_order)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pos, total_order, fa_order, fa_ordheader


        nonlocal s_order
        nonlocal s_order_list
        return {}

    fa_ordheader = db_session.query(Fa_ordheader).filter(
            (func.lower(Fa_ordheader.(order_nr).lower()) == (order_nr).lower())).first()

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
        fa_ordheader.modified_By = user_init
        fa_ordheader.modified_Date = billdate
        fa_ordheader.modified_Time = get_current_time_in_seconds()

        if fa_ordheader.approved_1 == False and appr_1 :
            fa_ordheader.Approved_1 = appr_1
            fa_ordheader.Approved_1_By = user_init
            fa_ordheader.Approved_1_Date = billdate
            fa_ordheader.Approved_1_time = get_current_time_in_seconds()
            fa_ordheader.Approved_2 = appr_1
            fa_ordheader.Approved_2_By = user_init
            fa_ordheader.Approved_2_Date = billdate
            fa_ordheader.Approved_2_time = get_current_time_in_seconds()
            fa_ordheader.Approved_3 = appr_1
            fa_ordheader.Approved_3_By = user_init
            fa_ordheader.Approved_3_Date = billdate
            fa_ordheader.Approved_3_time = get_current_time_in_seconds()

        if fa_ordheader.released_flag == False:

            if fa_ordheader.approved_1 :
                fa_ordheader.released_flag = True
                fa_ordheader.released_date = billdate
                fa_ordheader.released_time = get_current_time_in_seconds()

    for fa_order in db_session.query(Fa_order).filter(
            (func.lower(Fa_order.(order_nr).lower()) == (order_nr).lower())).all():
        db_session.delete(fa_order)

    for s_order in query(s_order_list):
        pos = pos + 1
        total_order = total_order + s_order.order_amount
        fa_order = Fa_order()
        db_session.add(fa_order)

        fa_order.order_nr = s_order.order_nr
        fa_order.Fa_Nr = s_order.fa_nr
        fa_order.Order_Qty = s_order.order_qty
        fa_order.Order_Price = s_order.order_price
        fa_order.Discount1 = s_order.discount1
        fa_order.Discount2 = s_order.discount2
        fa_order.VAT = s_order.vat
        fa_order.Order_Amount = s_order.order_amount
        fa_order.Fa_remarks = s_order.fa_remarks
        fa_order.statFlag = 0
        fa_order.Fa_Pos = pos
        fa_order.op_art = 2
        fa_order.last_ID = user_init


    fa_ordheader.total_amount = total_order

    return generate_output()