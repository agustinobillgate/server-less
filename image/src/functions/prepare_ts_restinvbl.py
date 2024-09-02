from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Printer, Htparam, Queasy, Waehrung, Hoteldpt, Kellner, H_bill, Bediener

def prepare_ts_restinvbl(pvilanguage:int, curr_dept:int, curr_printer:int, user_init_str:str, transdate:date):
    mealcoupon_cntrl = False
    must_print = False
    zero_flag = False
    multi_cash = False
    cancel_exist = False
    msg_str = ""
    disc_art1 = 0
    disc_art2 = 0
    disc_art3 = 0
    mi_ordertaker = False
    price_decimal = 0
    curr_local = ""
    curr_foreign = ""
    double_currency = False
    foreign_rate = False
    exchg_rate = 0
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
    lvcarea:str = "TS_restinv"
    user_init:str = ""
    from_acct:bool = False
    guest = printer = htparam = queasy = waehrung = hoteldpt = kellner = h_bill = bediener = None

    hbill = t_kellner = bill_guest = vhpusr = None

    hbill_list, Hbill = create_model("Hbill", {"kellner_nr":int})
    t_kellner_list, T_kellner = create_model("T_kellner", {"kellner_nr":int})

    Bill_guest = Guest
    Vhpusr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, hbill_list, t_kellner_list, lvcarea, user_init, from_acct, guest, printer, htparam, queasy, waehrung, hoteldpt, kellner, h_bill, bediener
        nonlocal bill_guest, vhpusr


        nonlocal hbill, t_kellner, bill_guest, vhpusr
        nonlocal hbill_list, t_kellner_list
        return {"mealcoupon_cntrl": mealcoupon_cntrl, "must_print": must_print, "zero_flag": zero_flag, "multi_cash": multi_cash, "cancel_exist": cancel_exist, "msg_str": msg_str, "disc_art1": disc_art1, "disc_art2": disc_art2, "disc_art3": disc_art3, "mi_ordertaker": mi_ordertaker, "price_decimal": price_decimal, "curr_local": curr_local, "curr_foreign": curr_foreign, "double_currency": double_currency, "foreign_rate": foreign_rate, "exchg_rate": exchg_rate, "b_title": b_title, "deptname": deptname, "p_223": p_223, "curr_waiter": curr_waiter, "fl_code": fl_code, "pos1": pos1, "pos2": pos2, "cashless_flag": cashless_flag, "hbill": hbill_list, "t-kellner": t_kellner_list}

    def chg_billdate(message_flag:bool):

        nonlocal mealcoupon_cntrl, must_print, zero_flag, multi_cash, cancel_exist, msg_str, disc_art1, disc_art2, disc_art3, mi_ordertaker, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, b_title, deptname, p_223, curr_waiter, fl_code, pos1, pos2, cashless_flag, hbill_list, t_kellner_list, lvcarea, user_init, from_acct, guest, printer, htparam, queasy, waehrung, hoteldpt, kellner, h_bill, bediener
        nonlocal bill_guest, vhpusr


        nonlocal hbill, t_kellner, bill_guest, vhpusr
        nonlocal hbill_list, t_kellner_list

        zugriff:bool = False
        datum:date = None
        Vhpusr = Bediener

        vhpusr = db_session.query(Vhpusr).filter(
                (func.lower(Vhpusr.userinit) == (user_init).lower())).first()

        if substring(vhpusr.permission, 14, 1) >= "1" or substring(vhpusr.permission, 37, 1) >= "1":
            datum = transdate
            fl_code = 1

        elif message_flag:
            msg_str = msg_str + chr(2) + translateExtended ("Sorry, no access right.", lvcarea, "")


    if num_entries(user_init_str, ";") > 1:
        user_init = entry(0, user_init_str, ";")
        from_acct = logical(entry(1, user_init_str, ";"))


    else:
        user_init = user_init_str

    printer = db_session.query(Printer).filter(
            (Printer.nr == curr_printer)).first()

    if not printer:
        msg_str = msg_str + chr(2) + translateExtended ("Number Printer ", lvcarea, "") + to_string(curr_printer) + translateExtended (" was not defined in Printer Administration.", lvcarea, "")

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 834)).first()
    cashless_flag = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 274)).first()
    mealcoupon_cntrl = flogical

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 877)).first()
    must_print = flogical

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 869)).first()
    zero_flag = flogical

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 833)).first()
    multi_cash = flogical

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 11)).first()
    cancel_exist = None != queasy

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 867)).first()

    bill_guest = db_session.query(Bill_guest).filter(
            (Bill_guest.gastnr == htparam.finteger)).first()

    if not bill_guest:
        msg_str = msg_str + chr(2) + translateExtended ("GuestNo (Param 867) for credit restaurant undefined", lvcarea, "") + chr(10) + translateExtended ("Posting not possible.", lvcarea, "")

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 557)).first()
    disc_art1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 596)).first()
    disc_art2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 556)).first()
    disc_art3 = htparam.finteger

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 10)).first()

    if not queasy:
        mi_ordertaker = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()
    curr_local = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()
    curr_foreign = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    if foreign_rate or double_currency:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == curr_dept)).first()
    b_title = hoteldpt.depart + " Bills"

    if waehrung:
        b_title = b_title + " / Today's Exchange Rate  ==  " + to_string(exchg_rate)
    deptname = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 300)).first()
    b_title = b_title + ";" + to_string(htparam.flogical)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 223)).first()
    p_223 = htparam.flogical
    curr_waiter = to_int(user_init)

    kellner = db_session.query(Kellner).filter(
            (Kellner_nr == curr_waiter) &  (Kellner.departement == curr_dept)).first()

    if not kellner:
        curr_waiter = 0

    if kellner:
        t_kellner = T_kellner()
        t_kellner_list.append(t_kellner)

        t_kellner_nr = kellner_nr

    if from_acct:
        chg_billdate(False)

    for h_bill in db_session.query(H_bill).filter(
            (H_bill.departement == curr_dept) &  (H_bill.flag == 0)).all():
        hbill = Hbill()
        hbill_list.append(hbill)

        hbill.kellner_nr = h_bill.kellner_nr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 337)).first()
    pos1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 338)).first()
    pos2 = htparam.finteger

    return generate_output()