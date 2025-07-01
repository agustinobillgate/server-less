#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_bill_line, H_bill, H_artikel, Guest, Htparam, Queasy, Waehrung, Artikel, Hoteldpt, Kellner, Tisch, Exrate

def prepare_ts_closeinv_1bl(pvilanguage:int, curr_dept:int, inp_rechnr:int, user_init:string, user_name:string, curr_printer:int):

    prepare_cache ([H_bill_line, Guest, Htparam, Waehrung, Artikel, Hoteldpt, Kellner, Tisch, Exrate])

    must_print = False
    rev_sign = 1
    cancel_exist = False
    price_decimal = 0
    curr_local = ""
    curr_foreign = ""
    double_currency = False
    foreign_rate = False
    exchg_rate = 1
    f_disc = 0
    b_artnr = 0
    b_title = ""
    deptname = ""
    curr_user = ""
    curr_waiter = 1
    tischnr = 0
    rechnr = 0
    pax = 0
    balance = to_decimal("0.0")
    balance_foreign = to_decimal("0.0")
    bcol = 2
    printed = ""
    bill_date = None
    kreditlimit = to_decimal("0.0")
    total_saldo = to_decimal("0.0")
    msg_str = ""
    msg_str1 = ""
    rec_kellner = 0
    rec_bill_guest = 0
    cashless_flag = False
    cashless_artnr = None
    multi_cash = False
    t_b_list_list = []
    t_h_bill_list = []
    t_h_artikel_list = []
    lvcarea:string = "TS-closeinv"
    fogl_date:date = None
    h_bill_line = h_bill = h_artikel = guest = htparam = queasy = waehrung = artikel = hoteldpt = kellner = tisch = exrate = None

    b_list = t_b_list = t_h_bill = t_h_artikel = bill_guest = None

    b_list_list, B_list = create_model_like(H_bill_line)
    t_b_list_list, T_b_list = create_model_like(B_list)
    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    Bill_guest = create_buffer("Bill_guest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, lvcarea, fogl_date, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal pvilanguage, curr_dept, inp_rechnr, user_init, user_name, curr_printer
        nonlocal bill_guest


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, bill_guest
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list

        return {"must_print": must_print, "rev_sign": rev_sign, "cancel_exist": cancel_exist, "price_decimal": price_decimal, "curr_local": curr_local, "curr_foreign": curr_foreign, "double_currency": double_currency, "foreign_rate": foreign_rate, "exchg_rate": exchg_rate, "f_disc": f_disc, "b_artnr": b_artnr, "b_title": b_title, "deptname": deptname, "curr_user": curr_user, "curr_waiter": curr_waiter, "tischnr": tischnr, "rechnr": rechnr, "pax": pax, "balance": balance, "balance_foreign": balance_foreign, "bcol": bcol, "printed": printed, "bill_date": bill_date, "kreditlimit": kreditlimit, "total_saldo": total_saldo, "msg_str": msg_str, "msg_str1": msg_str1, "rec_kellner": rec_kellner, "rec_bill_guest": rec_bill_guest, "cashless_flag": cashless_flag, "cashless_artnr": cashless_artnr, "multi_cash": multi_cash, "t-b-list": t_b_list_list, "t-h-bill": t_h_bill_list, "t-h-artikel": t_h_artikel_list}

    def determine_revsign():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, lvcarea, fogl_date, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal pvilanguage, curr_dept, inp_rechnr, user_init, user_name, curr_printer
        nonlocal bill_guest


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, bill_guest
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list

        s:Decimal = to_decimal("0.0")

        h_bill_line_obj_list = {}
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                 (H_bill_line.rechnr == inp_rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line._recid).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True


            s =  to_decimal(s) + to_decimal(h_bill_line.betrag)

        if s < 0:
            rev_sign = - 1


    def open_table():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, lvcarea, fogl_date, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal pvilanguage, curr_dept, inp_rechnr, user_init, user_name, curr_printer
        nonlocal bill_guest


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, bill_guest
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list


        create_blist()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 867)]})

        bill_guest = get_cache (Guest, {"gastnr": [(eq, htparam.finteger)]})
        kreditlimit =  to_decimal(bill_guest.kreditlimit)

        h_bill = get_cache (H_bill, {"departement": [(eq, curr_dept)],"rechnr": [(eq, inp_rechnr)],"flag": [(eq, 1)]})

        if h_bill:

            tisch = get_cache (Tisch, {"tischnr": [(eq, h_bill.tischnr)]})
            tischnr = tisch.tischnr
            rechnr = h_bill.rechnr
            disp_bill_line()
            pax = h_bill.belegung
            balance =  to_decimal(h_bill.saldo)
            balance_foreign =  to_decimal(h_bill.mwst[98])

            if balance <= kreditlimit:
                bcol = 2

            if h_bill.rgdruck == 0:
                printed = ""
            else:
                printed = "*"

            if double_currency:
                pass

            if h_bill.betriebsnr != 0:

                queasy = get_cache (Queasy, {"key": [(eq, 10)],"number1": [(eq, h_bill.betriebsnr)]})

                if queasy:
                    curr_user = trim(curr_user + " - " + queasy.char1)

            return


    def create_blist():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, lvcarea, fogl_date, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal pvilanguage, curr_dept, inp_rechnr, user_init, user_name, curr_printer
        nonlocal bill_guest


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, bill_guest
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list

        h_art = None
        create_it:bool = False
        H_art =  create_buffer("H_art",H_artikel)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == inp_rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line.waehrungsnr).all():
            create_it = True

            h_art = db_session.query(H_art).filter(
                     (H_art.artnr == h_bill_line.artnr) & (H_art.departement == h_bill_line.departement)).first()

            if (h_art and h_art.artart != 0) or h_bill_line.artnr == 0:

                b_list = query(b_list_list, filters=(lambda b_list: b_list.artnr == h_bill_line.artnr and b_list.betrag == - h_bill_line.betrag and b_list.bill_datum == h_bill_line.bill_datum), first=True)

                if b_list:
                    b_list_list.remove(b_list)
                    create_it = False
                else:
                    bill_date = h_bill_line.bill_datum

            if create_it:
                b_list = B_list()
                b_list_list.append(b_list)

                b_list.rechnr = inp_rechnr
                b_list.artnr = h_bill_line.artnr
                b_list.bezeich = h_bill_line.bezeich
                b_list.anzahl = h_bill_line.anzahl
                b_list.nettobetrag =  to_decimal(h_bill_line.nettobetrag)
                b_list.fremdwbetrag =  to_decimal(h_bill_line.fremdwbetrag)
                b_list.betrag =  to_decimal(h_bill_line.betrag)
                b_list.tischnr = h_bill_line.tischnr
                b_list.departement = h_bill_line.departement
                b_list.epreis =  to_decimal(h_bill_line.epreis)
                b_list.zeit = h_bill_line.zeit
                b_list.bill_datum = h_bill_line.bill_datum
                b_list.sysdate = h_bill_line.sysdate
                b_list.segmentcode = h_bill_line.segmentcode
                b_list.waehrungsnr = h_bill_line.waehrungsnr
                b_list.transferred = True

        if htparam.fdate != bill_date and double_currency:

            exrate = get_cache (Exrate, {"datum": [(eq, bill_date)]})

            if exrate:
                exchg_rate =  to_decimal(exrate.betrag)


    def disp_bill_line():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, lvcarea, fogl_date, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal pvilanguage, curr_dept, inp_rechnr, user_init, user_name, curr_printer
        nonlocal bill_guest


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, bill_guest
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list

        if double_currency:

            for b_list in query(b_list_list, filters=(lambda b_list: b_list.rechnr == h_bill.rechnr and b_list.departement == curr_dept), sort_by=[("sysdate",True),("zeit",True)]):
                t_b_list = T_b_list()
                t_b_list_list.append(t_b_list)

                buffer_copy(b_list, t_b_list)

        else:

            for b_list in query(b_list_list, filters=(lambda b_list: b_list.rechnr == h_bill.rechnr and b_list.departement == curr_dept), sort_by=[("sysdate",True),("zeit",True)]):
                t_b_list = T_b_list()
                t_b_list_list.append(t_b_list)

                buffer_copy(b_list, t_b_list)

    def cal_total_saldo():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, lvcarea, fogl_date, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal pvilanguage, curr_dept, inp_rechnr, user_init, user_name, curr_printer
        nonlocal bill_guest


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, bill_guest
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list


        total_saldo =  to_decimal("0")

        h_bill_line_obj_list = {}
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                 (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.artnr != 0)).order_by(H_bill_line._recid).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True


            total_saldo =  to_decimal(total_saldo) + to_decimal(h_bill_line.betrag)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 834)]})
    cashless_flag = htparam.flogical

    if cashless_flag:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 569)]})

        if htparam.paramnr != 0:
            cashless_artnr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 833)]})
    multi_cash = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1003)]})
    fogl_date = htparam.fdate

    h_bill_line = get_cache (H_bill_line, {"departement": [(eq, curr_dept)],"rechnr": [(eq, inp_rechnr)]})

    if h_bill_line and h_bill_line.bill_datum <= fogl_date:
        msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("Bill older than last transfer date to G/L (Param 1003).", lvcarea, "")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 877)]})
    must_print = htparam.flogical
    determine_revsign()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 867)]})

    bill_guest = get_cache (Guest, {"gastnr": [(eq, htparam.finteger)]})

    if not bill_guest:
        msg_str1 = msg_str1 + chr_unicode(2) + translateExtended ("GuestNo (Param 867) for credit restaurant undefined", lvcarea, "") + chr_unicode(10) + translateExtended ("Posting not possible.", lvcarea, "")

        return generate_output()

    queasy = get_cache (Queasy, {"key": [(eq, 11)]})
    cancel_exist = None != queasy

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})
    f_disc = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 596)]})

    h_artikel = get_cache (H_artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, curr_dept)]})

    if h_artikel:

        artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, curr_dept)]})

    if artikel:
        b_artnr = artikel.artnr

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})
    b_title = hoteldpt.depart

    if waehrung:
        b_title = b_title + " ! " + translateExtended ("Today's Exchange Rate", lvcarea, "") + " = " + to_string(exchg_rate)
    deptname = hoteldpt.depart

    htparam = get_cache (Htparam, {"paramnr": [(eq, 300)]})
    deptname = deptname + chr_unicode(3) + to_string(htparam.flogical)

    h_bill = get_cache (H_bill, {"rechnr": [(eq, inp_rechnr)],"departement": [(eq, curr_dept)]})

    if h_bill:

        kellner = get_cache (Kellner, {"kellner_nr": [(eq, h_bill.kellner_nr)],"departement": [(eq, h_bill.departement)]})

        if kellner:
            curr_user = kellner.kellnername
        else:
            curr_user = user_init + " " + user_name
        t_h_bill = T_h_bill()
        t_h_bill_list.append(t_h_bill)

        buffer_copy(h_bill, t_h_bill)
        t_h_bill.rec_id = h_bill._recid


    else:
        curr_user = user_init + " " + user_name

    if kellner:
        rec_kellner = kellner._recid

    if curr_printer != 0:
        curr_waiter = to_int(user_init)

    kellner = get_cache (Kellner, {"kellner_nr": [(eq, curr_waiter)],"departement": [(eq, curr_dept)]})
    open_table()
    cal_total_saldo()

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == curr_dept) & ((H_artikel.artart == 2) | (H_artikel.artart == 6) | (H_artikel.artart == 7) | (H_artikel.artart == 11) | (H_artikel.artart == 12))).order_by(H_artikel._recid).all():
        t_h_artikel = T_h_artikel()
        t_h_artikel_list.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = to_int(h_artikel._recid)

        if t_h_artikel.artnr == cashless_artnr:
            t_h_artikel.bezeich = replace_str(t_h_artikel.bezeich, " ", "")

    if bill_guest:
        rec_bill_guest = bill_guest._recid

    return generate_output()