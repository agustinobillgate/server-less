from functions.additional_functions import *
import decimal
from datetime import date
from models import H_bill_line, H_bill, H_artikel, Guest, Htparam, Queasy, Waehrung, Artikel, Hoteldpt, Kellner, Tisch, Exrate

def prepare_ts_closeinv_1bl(pvilanguage:int, curr_dept:int, inp_rechnr:int, user_init:str, user_name:str, curr_printer:int):
    must_print = False
    rev_sign = 0
    cancel_exist = False
    price_decimal = 0
    curr_local = ""
    curr_foreign = ""
    double_currency = False
    foreign_rate = False
    exchg_rate = 0
    f_disc = 0
    b_artnr = 0
    b_title = ""
    deptname = ""
    curr_user = ""
    curr_waiter = 0
    tischnr = 0
    rechnr = 0
    pax = 0
    balance = 0
    balance_foreign = 0
    bcol = 0
    printed = ""
    bill_date = None
    kreditlimit = 0
    total_saldo = 0
    msg_str = ""
    msg_str1 = ""
    rec_kellner = 0
    rec_bill_guest = 0
    cashless_flag = False
    cashless_artnr = 0
    multi_cash = False
    t_b_list_list = []
    t_h_bill_list = []
    t_h_artikel_list = []
    lvcarea:str = "TS_closeinv"
    fogl_date:date = None
    h_bill_line = h_bill = h_artikel = guest = htparam = queasy = waehrung = artikel = hoteldpt = kellner = tisch = exrate = None

    b_list = t_b_list = t_h_bill = t_h_artikel = bill_guest = h_art = None

    b_list_list, B_list = create_model_like(H_bill_line)
    t_b_list_list, T_b_list = create_model_like(B_list)
    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    Bill_guest = Guest
    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, lvcarea, fogl_date, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal bill_guest, h_art


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, bill_guest, h_art
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list
        return {"must_print": must_print, "rev_sign": rev_sign, "cancel_exist": cancel_exist, "price_decimal": price_decimal, "curr_local": curr_local, "curr_foreign": curr_foreign, "double_currency": double_currency, "foreign_rate": foreign_rate, "exchg_rate": exchg_rate, "f_disc": f_disc, "b_artnr": b_artnr, "b_title": b_title, "deptname": deptname, "curr_user": curr_user, "curr_waiter": curr_waiter, "tischnr": tischnr, "rechnr": rechnr, "pax": pax, "balance": balance, "balance_foreign": balance_foreign, "bcol": bcol, "printed": printed, "bill_date": bill_date, "kreditlimit": kreditlimit, "total_saldo": total_saldo, "msg_str": msg_str, "msg_str1": msg_str1, "rec_kellner": rec_kellner, "rec_bill_guest": rec_bill_guest, "cashless_flag": cashless_flag, "cashless_artnr": cashless_artnr, "multi_cash": multi_cash, "t-b-list": t_b_list_list, "t-h-bill": t_h_bill_list, "t-h-artikel": t_h_artikel_list}

    def determine_revsign():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, lvcarea, fogl_date, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal bill_guest, h_art


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, bill_guest, h_art
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list

        s:decimal = 0

        h_bill_line_obj_list = []
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement) &  (H_artikel.artart == 0)).filter(
                (H_bill_line.rechnr == inp_rechnr) &  (H_bill_line.departement == curr_dept)).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)


            s = s + h_bill_line.betrag

        if s < 0:
            rev_sign = - 1

    def open_table():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, lvcarea, fogl_date, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal bill_guest, h_art


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, bill_guest, h_art
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list


        create_blist()

        htparam = db_session.query(Htparam).filter(
                (htpara.paramnr == 867)).first()

        bill_guest = db_session.query(Bill_guest).filter(
                (Bill_guest.gastnr == htparam.finteger)).first()
        kreditlimit = bill_guest.kreditlimit

        h_bill = db_session.query(H_bill).filter(
                (H_bill.departement == curr_dept) &  (H_bill.rechnr == inp_rechnr) &  (H_bill.flag == 1)).first()

        if h_bill:

            tisch = db_session.query(Tisch).filter(
                    (tischnr == h_bill.tischnr)).first()
            tischnr = tischnr
            rechnr = h_bill.rechnr
            disp_bill_line()
            pax = h_bill.belegung
            balance = h_bill.saldo
            balance_foreign = h_bill.mwst[98]

            if balance <= kreditlimit:
                bcol = 2

            if h_bill.rgdruck == 0:
                printed = ""
            else:
                printed = "*"

            if double_currency:
                pass

            if h_bill.betriebsnr != 0:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 10) &  (Queasy.number1 == h_bill.betriebsnr)).first()

                if queasy:
                    curr_user = trim(curr_user + " - " + queasy.char1)

            return

    def create_blist():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, lvcarea, fogl_date, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal bill_guest, h_art


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, bill_guest, h_art
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list

        create_it:bool = False
        H_art = H_artikel

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        for h_bill_line in db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == inp_rechnr) &  (H_bill_line.departement == curr_dept)).all():
            create_it = True

            h_art = db_session.query(H_art).filter(
                    (H_art.artnr == h_bill_line.artnr) &  (H_art.departement == h_bill_line.departement)).first()

            if (h_art and h_art.artart != 0) or h_bill_line.artnr == 0:

                b_list = query(b_list_list, filters=(lambda b_list :b_list.artnr == h_bill_line.artnr and b_list.betrag == - h_bill_line.betrag and b_list.bill_datum == h_bill_line.bill_datum), first=True)

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
                b_list.nettobetrag = h_bill_line.nettobetrag
                b_list.fremdwbetrag = h_bill_line.fremdwbetrag
                b_list.betrag = h_bill_line.betrag
                b_list.tischnr = h_bill_line.tischnr
                b_list.departement = h_bill_line.departement
                b_list.epreis = h_bill_line.epreis
                b_list.zeit = h_bill_line.zeit
                b_list.bill_datum = h_bill_line.bill_datum
                b_list.sysdate = h_bill_line.sysdate
                b_list.segmentcode = h_bill_line.segmentcode
                b_list.waehrungsnr = h_bill_line.waehrungsnr
                b_list.transferred = True

        if htparam.fdate != bill_date and double_currency:

            exrate = db_session.query(Exrate).filter(
                    (Exrate.datum == bill_date)).first()

            if exrate:
                exchg_rate = exrate.betrag

    def disp_bill_line():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, lvcarea, fogl_date, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal bill_guest, h_art


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, bill_guest, h_art
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list

        if double_currency:

            for b_list in query(b_list_list, filters=(lambda b_list :b_list.rechnr == h_bill.rechnr and b_list.departement == curr_dept)):
                t_b_list = T_b_list()
                t_b_list_list.append(t_b_list)

                buffer_copy(b_list, t_b_list)

        else:

            for b_list in query(b_list_list, filters=(lambda b_list :b_list.rechnr == h_bill.rechnr and b_list.departement == curr_dept)):
                t_b_list = T_b_list()
                t_b_list_list.append(t_b_list)

                buffer_copy(b_list, t_b_list)


    def cal_total_saldo():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, lvcarea, fogl_date, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal bill_guest, h_art


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, bill_guest, h_art
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list


        total_saldo = 0

        h_bill_line_obj_list = []
        for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) &  (H_artikel.departement == H_bill_line.departement) &  (H_artikel.artart == 0)).filter(
                (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == h_bill.departement) &  (H_bill_line.artnr != 0)).all():
            if h_bill_line._recid in h_bill_line_obj_list:
                continue
            else:
                h_bill_line_obj_list.append(h_bill_line._recid)


            total_saldo = total_saldo + h_bill_line.betrag


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 834)).first()
    cashless_flag = htparam.flogical

    if cashless_flag:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 569)).first()

        if htparam.paramnr != 0:
            cashless_artnr = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 833)).first()
    multi_cash = flogical

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 1003)).first()
    fogl_date = htparam.fdate

    h_bill_line = db_session.query(H_bill_line).filter(
            (H_bill_line.departement == curr_dept) &  (H_bill_line.rechnr == inp_rechnr)).first()

    if h_bill_line and h_bill_line.bill_datum <= fogl_date:
        msg_str = msg_str + chr(2) + "&W" + translateExtended ("Bill older than last transfer date to G/L (Param 1003).", lvcarea, "")

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 877)).first()
    must_print = flogical
    determine_revsign()

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 867)).first()

    bill_guest = db_session.query(Bill_guest).filter(
            (Bill_guest.gastnr == htparam.finteger)).first()

    if not bill_guest:
        msg_str1 = msg_str1 + chr(2) + translateExtended ("GuestNo (Param 867) for credit restaurant undefined", lvcarea, "") + chr(10) + translateExtended ("Posting not possible.", lvcarea, "")

        return generate_output()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 11)).first()
    cancel_exist = None != queasy

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

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 557)).first()
    f_disc = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 596)).first()

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == htparam.finteger) &  (H_artikel.departement == curr_dept)).first()

    if h_artikel:

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == curr_dept)).first()

    if artikel:
        b_artnr = artikel.artnr

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == curr_dept)).first()
    b_title = hoteldpt.depart

    if waehrung:
        b_title = b_title + " ! " + translateExtended ("Today's Exchange Rate", lvcarea, "") + "  ==  " + to_string(exchg_rate)
    deptname = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 300)).first()
    deptname = deptname + chr(3) + to_string(htparam.flogical)

    h_bill = db_session.query(H_bill).filter(
            (H_bill.rechnr == inp_rechnr) &  (H_bill.departement == curr_dept)).first()

    if h_bill:

        kellner = db_session.query(Kellner).filter(
                (Kellner_nr == h_bill.kellner_nr) &  (Kellner.departement == h_bill.departement)).first()

        if kellner:
            curr_user = kellnername
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

    kellner = db_session.query(Kellner).filter(
            (Kellner_nr == curr_waiter) &  (Kellner.departement == curr_dept)).first()
    open_table()
    cal_total_saldo()

    for h_artikel in db_session.query(H_artikel).filter(
            (H_artikel.departement == curr_dept) &  ((H_artikel.artart == 2) |  (H_artikel.artart == 6) |  (H_artikel.artart == 7) |  (H_artikel.artart == 11) |  (H_artikel.artart == 12))).all():
        t_h_artikel = T_h_artikel()
        t_h_artikel_list.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = to_int(h_artikel._recid)

        if t_h_artikel.artnr == cashless_artnr:
            t_h_artikel.bezeich = replace_str(t_h_artikel.bezeich, " ", "")

    if bill_guest:
        rec_bill_guest = bill_guest._recid

    return generate_output()