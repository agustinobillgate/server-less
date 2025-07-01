#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Printer, Htparam, Queasy, Waehrung, Hoteldpt, Kellner, H_bill, Bediener

def prepare_ts_restinvbl(pvilanguage:int, curr_dept:int, curr_printer:int, user_init_str:string, transdate:date):

    prepare_cache ([Htparam, Waehrung, Hoteldpt, Kellner, H_bill, Bediener])

    mealcoupon_cntrl = False
    must_print = False
    zero_flag = False
    multi_cash = False
    cancel_exist = False
    msg_str = ""
    disc_art1 = 0
    disc_art2 = 0
    disc_art3 = 0
    mi_ordertaker = True
    price_decimal = 0
    curr_local = ""
    curr_foreign = ""
    double_currency = False
    foreign_rate = False
    exchg_rate = 1
    b_title = ""
    deptname = ""
    p_223 = False
    curr_waiter = 0
    fl_code = 0
    pos1 = 0
    pos2 = 0
    cashless_flag = False
    hbill_list = []
    t_kellner_list = []
    lvcarea:string = "TS-restinv"
    user_init:string = ""
    from_acct:bool = False
    guest = printer = htparam = queasy = waehrung = hoteldpt = kellner = h_bill = bediener = None

    hbill = t_kellner = bill_guest = None

    hbill_list, Hbill = create_model("Hbill", {"kellner_nr":int})
    t_kellner_list, T_kellner = create_model("T_kellner", {"kellner_nr":int})

    Bill_guest = create_buffer("Bill_guest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, hbill_list, t_kellner_list, lvcarea, user_init, from_acct, guest, printer, htparam, queasy, waehrung, hoteldpt, kellner, h_bill, bediener
        nonlocal pvilanguage, curr_dept, curr_printer, user_init_str, transdate
        nonlocal bill_guest


        nonlocal hbill, t_kellner, bill_guest
        nonlocal hbill_list, t_kellner_list

        return {"mealcoupon_cntrl": mealcoupon_cntrl, "must_print": must_print, "zero_flag": zero_flag, "multi_cash": multi_cash, "cancel_exist": cancel_exist, "msg_str": msg_str, "disc_art1": disc_art1, "disc_art2": disc_art2, "disc_art3": disc_art3, "mi_ordertaker": mi_ordertaker, "price_decimal": price_decimal, "curr_local": curr_local, "curr_foreign": curr_foreign, "double_currency": double_currency, "foreign_rate": foreign_rate, "exchg_rate": exchg_rate, "b_title": b_title, "deptname": deptname, "p_223": p_223, "curr_waiter": curr_waiter, "fl_code": fl_code, "pos1": pos1, "pos2": pos2, "cashless_flag": cashless_flag, "hbill": hbill_list, "t-kellner": t_kellner_list}

    def chg_billdate(message_flag:bool):

        nonlocal mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, hbill_list, t_kellner_list, lvcarea, user_init, from_acct, guest, printer, htparam, queasy, waehrung, hoteldpt, kellner, h_bill, bediener
        nonlocal pvilanguage, curr_dept, curr_printer, user_init_str, transdate
        nonlocal bill_guest


        nonlocal hbill, t_kellner, bill_guest
        nonlocal hbill_list, t_kellner_list

        zugriff:bool = False
        datum:date = None
        vhpusr = None
        Vhpusr =  create_buffer("Vhpusr",Bediener)

        vhpusr = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if substring(vhpusr.permission, 14, 1) >= ("1").lower()  or substring(vhpusr.permission, 37, 1) >= ("1").lower() :
            datum = transdate
            fl_code = 1

        elif message_flag:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Sorry, no access right.", lvcarea, "")

    if num_entries(user_init_str, ";") > 1:
        user_init = entry(0, user_init_str, ";")
        from_acct = logical(entry(1, user_init_str, ";"))


    else:
        user_init = user_init_str

    printer = get_cache (Printer, {"nr": [(eq, curr_printer)]})

    if not printer:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Number Printer ", lvcarea, "") + to_string(curr_printer) + translateExtended (" was not defined in Printer Administration.", lvcarea, "")

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 834)]})
    cashless_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 274)]})
    mealcoupon_cntrl = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 877)]})
    must_print = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 869)]})
    zero_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 833)]})
    multi_cash = htparam.flogical

    queasy = get_cache (Queasy, {"key": [(eq, 11)]})
    cancel_exist = None != queasy

    htparam = get_cache (Htparam, {"paramnr": [(eq, 867)]})

    bill_guest = db_session.query(Bill_guest).filter(
             (Bill_guest.gastnr == htparam.finteger)).first()

    if not bill_guest:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("GuestNo (Param 867) for credit restaurant undefined", lvcarea, "") + chr_unicode(10) + translateExtended ("Posting not possible.", lvcarea, "")

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
    disc_art1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})
    disc_art2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
    disc_art3 = htparam.finteger

    queasy = get_cache (Queasy, {"key": [(eq, 10)]})

    if not queasy:
        mi_ordertaker = False

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    curr_local = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})
    curr_foreign = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    if foreign_rate or double_currency:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})
    b_title = hoteldpt.depart + " Bills"

    if waehrung:
        b_title = b_title + " / Today's Exchange Rate = " + to_string(exchg_rate)
    deptname = hoteldpt.depart

    htparam = get_cache (Htparam, {"paramnr": [(eq, 300)]})
    b_title = b_title + ";" + to_string(htparam.flogical)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 223)]})
    p_223 = htparam.flogical
    curr_waiter = to_int(user_init)

    kellner = get_cache (Kellner, {"kellner_nr": [(eq, curr_waiter)],"departement": [(eq, curr_dept)]})

    if not kellner:
        curr_waiter = 0

    if kellner:
        t_kellner = T_kellner()
        t_kellner_list.append(t_kellner)

        t_kellner.kellner_nr = kellner.kellner_nr

    if from_acct:
        chg_billdate(False)

    for h_bill in db_session.query(H_bill).filter(
             (H_bill.departement == curr_dept) & (H_bill.flag == 0)).order_by(H_bill._recid).all():
        hbill = Hbill()
        hbill_list.append(hbill)

        hbill.kellner_nr = h_bill.kellner_nr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 337)]})
    pos1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 338)]})
    pos2 = htparam.finteger

    return generate_output()