# using conversion tools version: 1.0.0.117

# ============================================================
# Rulita, 27-11-2025
# - Added with_for_update all query
# - Fixing issue return generate_output() not correct position
# ============================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_order, Fa_ordheader, Queasy

from functions import log_program as log

s_order_data, S_order = create_model_like(
    Fa_order, {
        "nr_budget": int,
    }
)


def fa_chgpo_save_detail_webbl(s_order_data: [S_order], order_nr: string, credit_term: int, curr: int, dept_nr: int,
                               order_date: date, supplier_nr: int, _expected_delivery: date, order_type: string,
                               order_name: string, comments: string, user_init: string,
                               billdate: date, appr_1: bool):

    prepare_cache([Fa_ordheader])

    pos: int = 0
    total_order: Decimal = to_decimal("0.0")
    pr_nr: string = ""
    fa_order = fa_ordheader = queasy = None

    s_order = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pos, total_order, pr_nr, fa_order, fa_ordheader, queasy
        nonlocal order_nr, credit_term, curr, dept_nr, order_date, supplier_nr, _expected_delivery, order_type, order_name, comments, user_init, billdate, appr_1
        nonlocal s_order

        return {}

    # fa_ordheader = get_cache (Fa_ordheader, {"order_nr": [(eq, order_nr)]})
    fa_ordheader = db_session.query(Fa_ordheader).filter(
        (Fa_ordheader.order_nr == order_nr)).with_for_update().first()

    if fa_ordheader:
        fa_ordheader.order_nr = order_nr
        fa_ordheader.credit_term = credit_term
        fa_ordheader.currency = curr
        fa_ordheader.dept_nr = dept_nr
        fa_ordheader.order_date = order_date
        fa_ordheader.supplier_nr = supplier_nr
        fa_ordheader.expected_delivery = _expected_delivery
        fa_ordheader.order_type = order_type
        fa_ordheader.order_name = order_name
        fa_ordheader.order_desc = comments
        fa_ordheader.modified_by = user_init
        fa_ordheader.modified_date = billdate
        fa_ordheader.modified_time = get_current_time_in_seconds()
        pr_nr = fa_ordheader.pr_nr
        # Rulita, 27-11-2025 | Fixing issue return generate_output() not correct position
        # return generate_output()

        print(f"[DEBUG] set appr from {fa_ordheader.approved_1} to {appr_1}")
        if fa_ordheader.approved_1 == False and appr_1:
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
            print("[LOG] check release flag")
            if fa_ordheader.approved_1:
                fa_ordheader.released_flag = True
                print("[LOG] set released flag to True")
                fa_ordheader.released_date = billdate
                fa_ordheader.released_time = get_current_time_in_seconds()

    fa_order_data = (
        db_session.query(Fa_order).filter(
            (Fa_order.order_nr == (order_nr).lower())
        )
        .order_by(Fa_order._recid)
    )
    for fa_order in fa_order_data:
        db_session.delete(fa_order)

    queasy_data = (
        db_session.query(Queasy).filter(
            (Queasy.key == 315) &
            (Queasy.char1 == (order_nr).lower()) &
            (Queasy.char2 == (pr_nr).lower())
        )
        .order_by(Queasy._recid)
    )
    for queasy in queasy_data:
        db_session.delete(queasy)

    for s_order in query(s_order_data):
        pos = pos + 1
        total_order = to_decimal(total_order) + \
            to_decimal(s_order.order_amount)
        fa_order = Fa_order()
        db_session.add(fa_order)

        fa_order.order_nr = s_order.order_nr
        fa_order.fa_nr = s_order.fa_nr
        fa_order.order_qty = s_order.order_qty
        fa_order.order_price = to_decimal(s_order.order_price)
        fa_order.discount1 = to_decimal(s_order.discount1)
        fa_order.discount2 = to_decimal(s_order.discount2)
        fa_order.vat = to_decimal(s_order.vat)
        fa_order.order_amount = to_decimal(s_order.order_amount)
        fa_order.fa_remarks = s_order.fa_remarks
        fa_order.statflag = 0
        fa_order.fa_pos = pos
        fa_order.op_art = 2
        fa_order.last_id = user_init
        
        log.write_log("fa_chgpo_save_detail_webbl", f"[LOG] update detail fa_order: {s_order.__dict__}")

        # if s_order.ActiveReason != "" and s_order.ActiveReason != None:
        if s_order.activereason not in ("", None):
            fa_order.activereason = s_order.activereason
        else:
            fa_order.activereason = to_string(s_order.nr_budget)
    fa_ordheader.total_amount = to_decimal(total_order)

    return generate_output()
