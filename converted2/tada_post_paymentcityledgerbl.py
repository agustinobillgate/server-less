#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.tada_post_payment_getsaldobl import tada_post_payment_getsaldobl
from functions.tada_post_payment_preparebl import tada_post_payment_preparebl
from functions.tada_post_payment_btn_transferbl import tada_post_payment_btn_transferbl
from functions.tada_post_payment_updatebillbl import tada_post_payment_updatebillbl
from functions.tada_post_payment_restsale_updatehbillbl import tada_post_payment_restsale_updatehbillbl
from functions.tada_post_payment_delqueasybl import tada_post_payment_delqueasybl
from models import H_artikel, H_bill, Kellner, Queasy, Guest

def tada_post_paymentcityledgerbl(bill_no:int, dept_no:int, pay_type:int, tischnr:int, gname:string, pax:int, payment:Decimal, resno:int, reslinno:int, curr_room:string, user_init:string, vhp_note:string):

    prepare_cache ([H_bill, Queasy, Guest])

    rechnr = 0
    hbill_flag = 0
    result_msg = ""
    vsuccess = False
    language_code:int = 0
    rec_id:int = 0
    balance:Decimal = to_decimal("0.0")
    gastnr:int = 0
    order_name:string = ""
    order_phone:string = ""
    order_email:string = ""
    curr_gastnr:int = 0
    payment_param:int = 0
    saldo:Decimal = to_decimal("0.0")
    disc_art1:int = 0
    disc_art2:int = 0
    disc_art3:int = 0
    mi_ordertaker:bool = True
    price_decimal:int = 0
    curr_local:string = ""
    curr_foreign:string = ""
    foreign_rate:bool = False
    exchg_rate:Decimal = 1
    b_title:string = ""
    deptname:string = ""
    p_223:bool = False
    curr_waiter:int = 0
    fl_code:int = 0
    pos1:int = 0
    pos2:int = 0
    cashless_flag:bool = False
    c_param870:string = ""
    add_zeit:int = 0
    activate_deposit:bool = False
    bill_date:date = None
    p_88:bool = False
    amt:Decimal = to_decimal("0.0")
    amt_foreign:Decimal = to_decimal("0.0")
    msg_str:string = ""
    msg_str1:string = ""
    msg_str2:string = ""
    balance_foreign:Decimal = to_decimal("0.0")
    billart:int = 0
    qty:int = 0
    price:Decimal = to_decimal("0.0")
    amount_foreign:Decimal = to_decimal("0.0")
    amount:Decimal = to_decimal("0.0")
    description:string = ""
    transfer_zinr:string = ""
    cancel_flag:bool = False
    mwst:Decimal = to_decimal("0.0")
    mwst_foreign:Decimal = to_decimal("0.0")
    bcol:int = 0
    fl_code1:int = 0
    fl_code2:int = 0
    fl_code3:int = 0
    closed:bool = False
    mealcoupon_cntrl:bool = False
    must_print:bool = False
    zero_flag:bool = False
    multi_cash:bool = False
    cancel_exist:bool = False
    double_currency:bool = False
    dept_name:string = ""
    cancel_str:string = ""
    flag_code:int = 0
    var_testing:string = ""
    rec_id_h_artikel:int = 0
    service_code:int = 0
    h_artart:int = 0
    h_artnrfront:int = 0
    h_artikel = h_bill = kellner = queasy = guest = None

    hbill = t_kellner = t_h_artikel = t_submenu_list = t_h_bill = kellner1 = p_list = bguest = None

    hbill_data, Hbill = create_model("Hbill", {"kellner_nr":int})
    t_kellner_data, T_kellner = create_model("T_kellner", {"kellner_nr":int})
    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})
    t_submenu_list_data, T_submenu_list = create_model("T_submenu_list", {"menurecid":int, "zeit":int, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "zknr":int, "request":string})
    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    kellner1_data, Kellner1 = create_model_like(Kellner)
    p_list_data, P_list = create_model("P_list", {"rechnr":int, "dept":int, "billno":int, "printed_line":int, "b_recid":int, "last_amount":Decimal, "last_famount":Decimal})

    Bguest = create_buffer("Bguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rechnr, hbill_flag, result_msg, vsuccess, language_code, rec_id, balance, gastnr, order_name, order_phone, order_email, curr_gastnr, payment_param, saldo, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, c_param870, add_zeit, activate_deposit, bill_date, p_88, amt, amt_foreign, msg_str, msg_str1, msg_str2, balance_foreign, billart, qty, price, amount_foreign, amount, description, transfer_zinr, cancel_flag, mwst, mwst_foreign, bcol, fl_code1, fl_code2, fl_code3, closed, mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, double_currency, dept_name, cancel_str, flag_code, var_testing, rec_id_h_artikel, service_code, h_artart, h_artnrfront, h_artikel, h_bill, kellner, queasy, guest
        nonlocal bill_no, dept_no, pay_type, tischnr, gname, pax, payment, resno, reslinno, curr_room, user_init, vhp_note
        nonlocal bguest


        nonlocal hbill, t_kellner, t_h_artikel, t_submenu_list, t_h_bill, kellner1, p_list, bguest
        nonlocal hbill_data, t_kellner_data, t_h_artikel_data, t_submenu_list_data, t_h_bill_data, kellner1_data, p_list_data

        return {"rechnr": rechnr, "hbill_flag": hbill_flag, "result_msg": result_msg, "vsuccess": vsuccess}

    if num_entries(gname, "|") >= 2:
        order_name = entry(0, gname, "|")
        order_phone = entry(1, gname, "|")
        order_email = entry(2, gname, "|")
    gname = order_name

    h_bill = get_cache (H_bill, {"rechnr": [(eq, bill_no)],"departement": [(eq, dept_no)]})

    if h_bill:
        rec_id = h_bill._recid
        balance =  to_decimal(h_bill.saldo)

    queasy = get_cache (Queasy, {"key": [(eq, 270)],"number1": [(eq, 1)],"betriebsnr": [(eq, 1)],"number2": [(eq, 26)]})

    if queasy:
        payment_param = to_int(queasy.char2)
    else:
        result_msg = "Artikel Number For Guest Ledger Not Available! Please Contact VHP Support!"

        return generate_output()

    guest = get_cache (Guest, {"mobil_telefon": [(eq, order_phone)],"karteityp": [(eq, 0)]})

    if not guest:

        guest = get_cache (Guest, {"telefon": [(eq, order_phone)],"karteityp": [(eq, 0)]})

        if not guest:

            for bguest in db_session.query(Bguest).order_by(Bguest.gastnr.desc()).yield_per(100):
                curr_gastnr = bguest.gastnr
                break

            if curr_gastnr == 0:
                curr_gastnr = 1
            else:
                curr_gastnr = curr_gastnr + 1
            guest = Guest()
            db_session.add(guest)

            guest.karteityp = 0
            guest.name = order_name
            guest.email_adr = order_email
            guest.telefon = order_phone
            guest.mobil_telefon = order_phone
            guest.gastnr = curr_gastnr
            guest.zahlungsart = payment_param
            guest.point_gastnr = payment_param
            gastnr = curr_gastnr
        else:
            gastnr = guest.gastnr
            guest.name = order_name
            guest.email_adr = order_email
            guest.telefon = order_phone
            guest.mobil_telefon = order_phone
            guest.zahlungsart = payment_param
            guest.point_gastnr = payment_param
    else:
        gastnr = guest.gastnr
        guest.name = order_name
        guest.email_adr = order_email
        guest.telefon = order_phone
        guest.mobil_telefon = order_phone
        guest.zahlungsart = payment_param
        guest.point_gastnr = payment_param
    pass

    if curr_room == None:
        curr_room = ""

    if gname == None:
        gname = ""
    saldo = get_output(tada_post_payment_getsaldobl(bill_no, dept_no))

    if balance != saldo:
        result_msg = "There is a new article posted, balance to be different." + chr_unicode(10) + "Please check the bill."

        return generate_output()
    mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, c_param870, activate_deposit, hbill_data, t_kellner_data = get_output(tada_post_payment_preparebl(language_code, dept_no, 1, user_init, None))

    if msg_str != "":
        result_msg = substring(msg_str, 1)

        return generate_output()

    t_kellner = query(t_kellner_data, first=True)
    billart, qty, description, price, amount_foreign, amount, bill_date, fl_code, fl_code1, msg_str, var_testing, t_h_artikel_data = get_output(tada_post_payment_btn_transferbl(language_code, rec_id, gastnr, dept_no, payment, exchg_rate, price_decimal, balance, None, disc_art1, disc_art2, disc_art3, t_kellner.kellner_nr))
    description = description + "/" + vhp_note

    if msg_str != "":
        result_msg = msg_str

        return generate_output()

    if fl_code1 == 1:
        result_msg = "payment with Voucher is not support"

        return generate_output()

    if fl_code == 2:
        result_msg = "NOT DEFINED: F/O Article" + " " + to_string(billart) + chr_unicode(10) + "C/L Posting not possible."

        return generate_output()

    elif fl_code == 3:

        return generate_output()

    elif fl_code == 1:

        t_h_artikel = query(t_h_artikel_data, first=True)

        if t_h_artikel:
            rec_id_h_artikel = t_h_artikel.rec_id
            service_code = t_h_artikel.service_code
            h_artart = t_h_artikel.artart
            h_artnrfront = t_h_artikel.artnrfront


        add_zeit = 1
        bill_date, cancel_flag, fl_code, mwst, mwst_foreign, rechnr, balance, bcol, balance_foreign, fl_code1, fl_code2, fl_code3, p_88, closed, t_h_bill_data, kellner1_data = get_output(tada_post_payment_updatebillbl(language_code, rec_id, rec_id_h_artikel, deptname, None, h_artart, False, service_code, payment, amount_foreign, price, double_currency, qty, exchg_rate, price_decimal, user_init, tischnr, dept_no, user_init, gname, pax, 0, add_zeit, billart, description, "", "", "", "", "", "", True, False, h_artnrfront, pay_type, gastnr, "", False, foreign_rate, curr_room, user_init, resno, reslinno, t_submenu_list_data))

        t_h_bill = query(t_h_bill_data, first=True)

        kellner1 = query(kellner1_data, first=True)

        if t_h_bill:
            rechnr = t_h_bill.rechnr
            hbill_flag = t_h_bill.flag

        if hbill_flag == 1:
            get_output(tada_post_payment_restsale_updatehbillbl(t_h_bill.rec_id))
        p_list_data = get_output(tada_post_payment_delqueasybl(p_list_data, t_h_bill.rec_id, False))
        vsuccess = True

    return generate_output()