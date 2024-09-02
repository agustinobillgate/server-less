from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Fa_order, Waehrung, Fa_ordheader, Htparam, Fa_counter

def fa_mkpo_btn_gobl(tfa_order:[Tfa_order], cmb_curr_screen_value:str, local_nr:int, order_nr:str, pr_nr:str, order_date:date, order_type:str, order_name:str, comments:str, supplier_nr:int, dept_nr:int, credit_term:int, paymentdate:date, expected_delivery:date, user_init:str, billdate:date, t_amount:decimal, appr_1:bool, answer:bool):
    curr:int = 0
    repos:int = 0
    fa_order = waehrung = fa_ordheader = htparam = fa_counter = None

    tfa_order = fa_orderhdr1 = None

    tfa_order_list, Tfa_order = create_model_like(Fa_order)

    Fa_orderhdr1 = Fa_ordheader

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr, repos, fa_order, waehrung, fa_ordheader, htparam, fa_counter
        nonlocal fa_orderhdr1


        nonlocal tfa_order, fa_orderhdr1
        nonlocal tfa_order_list
        return {}

    def re_numbering():

        nonlocal curr, repos, fa_order, waehrung, fa_ordheader, htparam, fa_counter
        nonlocal fa_orderhdr1


        nonlocal tfa_order, fa_orderhdr1
        nonlocal tfa_order_list

        thereis:bool = True
        while thereis  :

            fa_ordheader = db_session.query(Fa_ordheader).filter(
                    (func.lower(Fa_ordheader.(order_nr).lower()) == (order_nr).lower())).first()

            if fa_ordheader:
                thereis = True
                new_fapo_number()
                update_counters()
            else:
                thereis = False
                new_fapo_number()
                update_counters()

    def new_fapo_number():

        nonlocal curr, repos, fa_order, waehrung, fa_ordheader, htparam, fa_counter
        nonlocal fa_orderhdr1


        nonlocal tfa_order, fa_orderhdr1
        nonlocal tfa_order_list

        s:str = ""
        i:int = 1
        mm:int = 0
        yy:int = 0
        dd:int = 0
        docu_nr:str = ""
        a:bool = False
        Fa_orderhdr1 = Fa_ordheader

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 973)).first()

        if htparam.paramgruppe == 21:
            mm = get_month(billdate)
            yy = get_year(billdate)
            dd = get_day(billdate)
            s = "F" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99")

            if htparam.flogical:

                fa_counter = db_session.query(Fa_counter).filter(
                        (Fa_counter.count_type == 0) &  (Fa_counter.yy == yy) &  (Fa_counter.mm == mm) &  (Fa_counter.dd == dd) &  (Fa_counter.docu_type == 0)).first()

                if not fa_counter:
                    fa_counter = Fa_counter()
                    db_session.add(fa_counter)

                    fa_counter.count_type = 0
                    fa_counter.yy = yy
                    fa_counter.mm = mm
                    fa_counter.dd = dd
                    fa_counter.counters = 0
                    fa_counter.docu_type = 0

                fa_counter = db_session.query(Fa_counter).first()
                i = fa_counter.counters + 1
                docu_nr = s + to_string(dd, "99") + to_string(i, "999")
            else:

                fa_counter = db_session.query(Fa_counter).filter(
                        (Fa_counter.count_type == 1) &  (Fa_counter.yy == yy) &  (Fa_counter.mm == mm) &  (Fa_counter.docu_type == 0)).first()

                if not fa_counter:
                    fa_counter = Fa_counter()
                    db_session.add(fa_counter)

                    fa_counter.count_type = 1
                    fa_counter.yy = yy
                    fa_counter.mm = mm
                    fa_counter.dd = 0
                    fa_counter.counters = 0
                    fa_counter.docu_type = 0

                fa_counter = db_session.query(Fa_counter).first()
                i = fa_counter.counters + 1
                docu_nr = s + to_string(i, "99999")
        order_nr = docu_nr

    def update_counters():

        nonlocal curr, repos, fa_order, waehrung, fa_ordheader, htparam, fa_counter
        nonlocal fa_orderhdr1


        nonlocal tfa_order, fa_orderhdr1
        nonlocal tfa_order_list

        s:str = ""
        i:int = 1
        mm:int = 0
        yy:int = 0
        dd:int = 0
        docu_nr:str = ""
        a:bool = False
        a = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 973)).first()

        if htparam.paramgruppe == 21:
            mm = get_month(billdate)
            yy = get_year(billdate)
            dd = get_day(billdate)
            s = "F" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99")

            if htparam.flogical:

                fa_counter = db_session.query(Fa_counter).filter(
                        (Fa_counter.count_type == 0) &  (Fa_counter.yy == yy) &  (Fa_counter.mm == mm) &  (Fa_counter.dd == dd) &  (Fa_counter.docu_type == 0)).first()

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

                    fa_counter = db_session.query(Fa_counter).first()
                    fa_counter.counters = fa_counter.counters + 1

                    fa_counter = db_session.query(Fa_counter).first()
            else:

                fa_counter = db_session.query(Fa_counter).filter(
                        (Fa_counter.count_type == 1) &  (Fa_counter.yy == yy) &  (Fa_counter.mm == mm) &  (Fa_counter.docu_type == 0)).first()

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

                    fa_counter = db_session.query(Fa_counter).first()
                    fa_counter.counters = fa_counter.counters + 1

                    fa_counter = db_session.query(Fa_counter).first()

    tfa_order = query(tfa_order_list, first=True)

    waehrung = db_session.query(Waehrung).filter(
            (func.lower(Waehrung.wabkurz) == (cmb_curr_screen_value).lower())).first()

    if waehrung:
        curr = waehrungsnr
    else:
        curr = local_nr
    re_numbering()
    fa_ordheader = Fa_ordheader()
    db_session.add(fa_ordheader)

    fa_ordheader.order_nr = order_nr
    fa_ordheader.pr_nr = pr_nr
    fa_ordheader.order_date = order_date
    fa_ordheader.order_type = order_type
    fa_ordheader.order_name = order_name
    fa_ordheader.Order_Desc = comments
    fa_ordheader.supplier_nr = supplier_nr
    fa_ordheader.dept_nr = dept_nr
    fa_ordheader.credit_term = credit_term
    fa_ordheader.currency = curr
    fa_ordheader.paymentdate = paymentdate
    fa_ordheader.expected_delivery = expected_delivery
    fa_ordheader.created_by = user_init
    fa_ordheader.Created_Date = billdate
    fa_ordheader.Created_Time = get_current_time_in_seconds()
    fa_ordheader.ActiveFlag = 0
    fa_ordheader.statFlag = 0
    fa_ordheader.printed = None
    fa_ordheader.total_Amount = t_amount

    if appr_1 :
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
        fa_ordheader.released_flag = True
        fa_ordheader.released_by = user_init
        fa_ordheader.released_date = billdate


        fa_ordheader.released_time = get_current_time_in_seconds()

    for tfa_order in query(tfa_order_list):
        repos = repos + 1
        fa_order = Fa_order()
        db_session.add(fa_order)

        fa_order.order_nr = order_nr
        fa_order.Fa_Nr = tfa_order.Fa_Nr
        fa_order.Order_Qty = tfa_order.Order_Qty
        fa_order.Order_Price = tfa_order.Order_Price
        fa_order.Discount1 = tfa_order.Discount1
        fa_order.Discount2 = tfa_order.Discount2
        fa_order.VAT = tfa_order.VAT
        fa_order.Order_Amount = tfa_order.Order_Amount
        fa_order.Fa_remarks = tfa_order.Fa_remarks
        fa_order.Create_By = tfa_order.Create_By
        fa_order.Create_Date = tfa_order.Create_Date
        fa_order.Create_Time = tfa_order.Create_Time
        fa_order.statFlag = tfa_order.statFlag
        fa_order.Fa_Pos = repos
        fa_order.op_art = tfa_order.op_art
        fa_order.activeflag = 0
        fa_order.create_by = user_init
        fa_order.CREATE_date = billdate
        fa_order.create_time = get_current_time_in_seconds()


        tfa_order_list.remove(tfa_order)

    if not (appr_1 ):

        if answer:
            appr_1 = True


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
            fa_ordheader.released_flag = True
            fa_ordheader.released_by = user_init
            fa_ordheader.released_date = billdate
            fa_ordheader.released_time = get_current_time_in_seconds()


    else:
        print_it()

    return generate_output()