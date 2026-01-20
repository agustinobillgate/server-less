# using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 27-11-2025
# - Added with_for_update all query
# - Fix progress not declare procedure print-it
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_order, Waehrung, Fa_ordheader, Htparam, Fa_counter

from functions import log_program as log

tfa_order_data, Tfa_order = create_model_like(
    Fa_order, {
        "nr_budget": int
    })


def fa_mkpo_btn_go_webbl(tfa_order_data: [Tfa_order], cmb_curr_screen_value: string, local_nr: int, order_nr: string, pr_nr: string, order_date: date, order_type: string, order_name: string, comments: string, supplier_nr: int, dept_nr: int, credit_term: int, paymentdate: date, _expected_delivery: date, user_init: string, billdate: date, t_amount: Decimal, appr_1: bool, answer: bool):

    prepare_cache([Fa_order, Waehrung, Fa_ordheader, Htparam, Fa_counter])

    curr: int = 0
    repos: int = 0
    fa_order = waehrung = fa_ordheader = htparam = fa_counter = None

    tfa_order = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr, repos, fa_order, waehrung, fa_ordheader, htparam, fa_counter
        nonlocal cmb_curr_screen_value, local_nr, order_nr, pr_nr, order_date, order_type, order_name, comments, supplier_nr, dept_nr, credit_term, paymentdate, _expected_delivery, user_init, billdate, t_amount, appr_1, answer
        nonlocal tfa_order
        
        return {}

    def re_numbering():
        nonlocal curr, repos, fa_order, waehrung, fa_ordheader, htparam, fa_counter
        nonlocal cmb_curr_screen_value, local_nr, order_nr, pr_nr, order_date, order_type, order_name, comments, supplier_nr, dept_nr, credit_term, paymentdate, _expected_delivery, user_init, billdate, t_amount, appr_1, answer
        nonlocal tfa_order

        thereis: bool = True
        while thereis:

            fa_ordheader = get_cache(
                Fa_ordheader, {"order_nr": [(eq, order_nr)]})

            if fa_ordheader:
                print(f"[RE_NUMBERING] fa_ordheader: {fa_ordheader.order_nr}")
                
                thereis = True
                new_fapo_number()
                update_counters()
            else:
                thereis = False
                new_fapo_number()
                update_counters()
                
        

    def new_fapo_number():
        nonlocal curr, repos, fa_order, waehrung, fa_ordheader, htparam, fa_counter
        nonlocal cmb_curr_screen_value, local_nr, order_nr, pr_nr, order_date, order_type, order_name, comments, supplier_nr, dept_nr, credit_term, paymentdate, _expected_delivery, user_init, billdate, t_amount, appr_1, answer
        nonlocal tfa_order

        fa_orderhdr1 = None
        s: string = ""
        i: int = 1
        mm: int = 0
        yy: int = 0
        dd: int = 0
        docu_nr: string = ""
        a: bool = False
        Fa_orderhdr1 = create_buffer("Fa_orderhdr1", Fa_ordheader)

        htparam = get_cache(Htparam, {"paramnr": [(eq, 973)]})

        if htparam.paramgruppe == 21:
            mm = get_month(billdate)
            yy = get_year(billdate)
            dd = get_day(billdate)
            s = "F" + substring(to_string(get_year(billdate)),
                                2, 2) + to_string(get_month(billdate), "99")

            if htparam.flogical:

                # fa_counter = get_cache (Fa_counter, {"count_type": [(eq, 0)],"yy": [(eq, yy)],"mm": [(eq, mm)],"dd": [(eq, dd)],"docu_type": [(eq, 0)]})
                fa_counter = (
                    db_session.query(Fa_counter)
                    .filter(
                        (Fa_counter.count_type == 0) &
                        (Fa_counter.yy == yy) &
                        (Fa_counter.mm == mm) &
                        (Fa_counter.dd == dd) &
                        (Fa_counter.docu_type == 0)
                    )
                    .with_for_update()
                    .first())

                if not fa_counter:
                    fa_counter = Fa_counter()
                    db_session.add(fa_counter)

                    fa_counter.count_type = 0
                    fa_counter.yy = yy
                    fa_counter.mm = mm
                    fa_counter.dd = dd
                    fa_counter.counters = 0
                    fa_counter.docu_type = 0
                    
                    print(f"[LOG] new fa_counter: {fa_counter.counters}")

                else:
                    i = fa_counter.counters + 1
                    docu_nr = s + to_string(dd, "99") + to_string(i, "999")
                    
                    print(f"[LOG] check docu_nr: {docu_nr}")
                    
            else:

                # fa_counter = get_cache (Fa_counter, {"count_type": [(eq, 1)],"yy": [(eq, yy)],"mm": [(eq, mm)],"docu_type": [(eq, 0)]})
                fa_counter = (
                    db_session.query(Fa_counter)
                    .filter(
                        (Fa_counter.count_type == 1) &
                        (Fa_counter.yy == yy) &
                        (Fa_counter.mm == mm) &
                        (Fa_counter.docu_type == 0)
                    )
                    .with_for_update()
                    .first())

                if not fa_counter:
                    fa_counter = Fa_counter()
                    db_session.add(fa_counter)

                    fa_counter.count_type = 1
                    fa_counter.yy = yy
                    fa_counter.mm = mm
                    fa_counter.dd = 0
                    fa_counter.counters = 0
                    fa_counter.docu_type = 0
                    
                    print(f"[LOG] new fa_counter: {fa_counter.counters}")

                pass
                i = fa_counter.counters + 1
                docu_nr = s + to_string(i, "99999")
                
        order_nr = docu_nr
        print(f"[LOG] counter: {fa_counter.counters} | docu_nr: {docu_nr}")
        

    def update_counters():
        nonlocal curr, repos, fa_order, waehrung, fa_ordheader, htparam, fa_counter
        nonlocal cmb_curr_screen_value, local_nr, order_nr, pr_nr, order_date, order_type, order_name, comments, supplier_nr, dept_nr, credit_term, paymentdate, _expected_delivery, user_init, billdate, t_amount, appr_1, answer
        nonlocal tfa_order

        s: string = ""
        i: int = 1
        mm: int = 0
        yy: int = 0
        dd: int = 0
        docu_nr: string = ""
        a: bool = False
        a = True

        htparam = get_cache(Htparam, {"paramnr": [(eq, 973)]})

        if htparam.paramgruppe == 21:
            mm = get_month(billdate)
            yy = get_year(billdate)
            dd = get_day(billdate)
            s = "F" + substring(to_string(get_year(billdate)),
                                2, 2) + to_string(get_month(billdate), "99")

            if htparam.flogical:

                # fa_counter = get_cache (Fa_counter, {"count_type": [(eq, 0)],"yy": [(eq, yy)],"mm": [(eq, mm)],"dd": [(eq, dd)],"docu_type": [(eq, 0)]})
                fa_counter = (
                    db_session.query(Fa_counter).filter(
                        (Fa_counter.count_type == 0) &
                        (Fa_counter.yy == yy) &
                        (Fa_counter.mm == mm) &
                        (Fa_counter.dd == dd) &
                        (Fa_counter.docu_type == 0)
                    )
                    .with_for_update()
                    .first())

                if not fa_counter:
                    fa_counter = Fa_counter()
                    db_session.add(fa_counter)

                    fa_counter.count_type = 0
                    fa_counter.yy = yy
                    fa_counter.mm = mm
                    fa_counter.dd = dd
                    fa_counter.counters = 0
                    fa_counter.docu_type = 0

                else:
                    # pass
                    fa_counter.counters = fa_counter.counters + 1
                    # db_session.refresh(fa_counter, with_for_update=True)
                    # pass
            else:

                # fa_counter = get_cache (Fa_counter, {"count_type": [(eq, 1)],"yy": [(eq, yy)],"mm": [(eq, mm)],"docu_type": [(eq, 0)]})
                fa_counter = (
                    db_session.query(Fa_counter).filter(
                        (Fa_counter.count_type == 1) &
                        (Fa_counter.yy == yy) &
                        (Fa_counter.mm == mm) &
                        (Fa_counter.docu_type == 0)
                    )
                    .with_for_update()
                    .first())

                if not fa_counter:
                    fa_counter = Fa_counter()
                    db_session.add(fa_counter)

                    fa_counter.count_type = 1
                    fa_counter.yy = yy
                    fa_counter.mm = mm
                    fa_counter.dd = 0
                    fa_counter.counters = 0
                    fa_counter.docu_type = 0

                else:
                    # pass
                    fa_counter.counters = fa_counter.counters + 1
                    # pass
                    # db_session.refresh(fa_counter, with_for_update=True)
            
            print(f"[UPDATE_COUNTERS] fa_counter: {fa_counter.counters}")

    tfa_order = query(tfa_order_data, first=True)

    # waehrung = get_cache(Waehrung, {"wabkurz": [(eq, cmb_curr_screen_value)]})
    waehrung = db_session.query(Waehrung).filter(
        Waehrung.wabkurz == cmb_curr_screen_value).first()

    if waehrung:
        curr = waehrung.waehrungsnr
    else:
        curr = local_nr
    re_numbering()
    
    fa_ordheader = Fa_ordheader()
    db_session.add(fa_ordheader)

    fa_ordheader.order_nr = order_nr.strip()
    fa_ordheader.pr_nr = pr_nr
    fa_ordheader.order_date = order_date
    fa_ordheader.order_type = order_type
    fa_ordheader.order_name = order_name
    fa_ordheader.order_desc = comments
    fa_ordheader.supplier_nr = supplier_nr
    fa_ordheader.dept_nr = dept_nr
    fa_ordheader.credit_term = credit_term
    fa_ordheader.currency = curr
    fa_ordheader.paymentdate = paymentdate
    print(f"[LOG] expected date: {_expected_delivery}")
    fa_ordheader.expected_delivery = _expected_delivery
    fa_ordheader.created_by = user_init
    fa_ordheader.created_date = billdate
    fa_ordheader.created_time = get_current_time_in_seconds()
    fa_ordheader.activeflag = 0
    fa_ordheader.statflag = 0
    fa_ordheader.printed = None
    fa_ordheader.total_amount = to_decimal(t_amount)
    
    log.write_log("fa_mkpo_btn_go_webbl", f"[LOG] new purchase order header: {fa_ordheader.__dict__}")

    
    for tfa_order in query(tfa_order_data, sort_by=[("fa_pos", False)]):
        
        print(f"[LOG] fa_number: {tfa_order.fa_nr}")
        repos = repos + 1
        fa_order = Fa_order()
        db_session.add(fa_order)

        fa_order.order_nr = order_nr
        fa_order.fa_nr = tfa_order.fa_nr
        fa_order.order_qty = tfa_order.order_qty
        fa_order.order_price = to_decimal(tfa_order.order_price)
        fa_order.discount1 = to_decimal(tfa_order.discount1)
        fa_order.discount2 = to_decimal(tfa_order.discount2)
        fa_order.vat = to_decimal(tfa_order.vat)
        fa_order.order_amount = to_decimal(tfa_order.order_amount)
        fa_order.fa_remarks = tfa_order.fa_remarks
        fa_order.create_by = tfa_order.create_by
        fa_order.create_date = tfa_order.create_date
        fa_order.create_time = tfa_order.create_time
        fa_order.statflag = tfa_order.statflag
        fa_order.fa_pos = repos
        fa_order.op_art = tfa_order.op_art
        fa_order.activeflag = 0
        fa_order.create_by = user_init
        fa_order.create_date = billdate
        fa_order.create_time = get_current_time_in_seconds()
        fa_order.activereason = to_string(tfa_order.nr_budget)
        
        log.write_log("fa_mkpo_btn_go_webbl", f"[LOG] new purchase order: {fa_order.__dict__}")

        tfa_order_data.remove(tfa_order)
        
    if appr_1:
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
        fa_ordheader.released_flag = True
        fa_ordheader.released_by = user_init
        fa_ordheader.released_date = billdate

        fa_ordheader.released_time = get_current_time_in_seconds()

    elif not appr_1:

        if answer:
            appr_1 = True

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
            fa_ordheader.released_flag = True
            fa_ordheader.released_by = user_init
            fa_ordheader.released_date = billdate
            fa_ordheader.released_time = get_current_time_in_seconds()

    # Rulita, 27-11-2025 | Fix progress not declare procedure print-it
    # else:
    #     print_it()

    return generate_output()
