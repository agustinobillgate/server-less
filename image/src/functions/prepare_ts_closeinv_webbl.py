from functions.additional_functions import *
import decimal
from datetime import date
from functions.htplogic import htplogic
from models import H_bill_line, H_bill, H_artikel, Guest, Htparam, Queasy, Waehrung, Artikel, Hoteldpt, Kellner, Tisch, Exrate

def prepare_ts_closeinv_webbl(pvilanguage:int, curr_dept:int, inp_rechnr:int, user_init:str, user_name:str, curr_printer:int):
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
    summary_bill_list = []
    lvcarea:str = "TS_closeinv"
    fogl_date:date = None
    t_serv_perc:decimal = 0
    t_mwst_perc:decimal = 0
    t_fact:decimal = 1
    t_service:decimal = 0
    t_mwst1:decimal = 0
    t_mwst:decimal = 0
    h_service:decimal = 0
    h_mwst:decimal = 0
    h_mwst2:decimal = 0
    t_h_service:decimal = 0
    t_h_mwst:decimal = 0
    t_h_mwst2:decimal = 0
    incl_service:bool = False
    incl_mwst:bool = False
    gst_logic:bool = False
    serv_disc:bool = True
    vat_disc:bool = True
    f_discart:int = -1
    amount:decimal = 0
    f_dec:decimal = 0
    serv_code:int = 0
    vat_code:int = 0
    servtax_use_foart:bool = False
    serv_vat:bool = False
    tax_vat:bool = False
    ct:str = ""
    l_deci:int = 2
    fact_scvat:decimal = 1
    service:decimal = 0
    vat:decimal = 0
    vat2:decimal = 0
    mwst:decimal = 0
    mwst1:decimal = 0
    sub_tot:decimal = 0
    tot_serv:decimal = 0
    tot_tax:decimal = 0
    grand_tot:decimal = 0
    netto_bet:decimal = 0
    compli_flag:bool = False
    h_bill_line = h_bill = h_artikel = guest = htparam = queasy = waehrung = artikel = hoteldpt = kellner = tisch = exrate = None

    b_list = t_b_list = t_h_bill = t_h_artikel = ordered_item = summary_bill = bill_guest = buff_hart = h_art = None

    b_list_list, B_list = create_model_like(H_bill_line)
    t_b_list_list, T_b_list = create_model_like(B_list)
    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})
    ordered_item_list, Ordered_item = create_model("Ordered_item", {"dept":int, "artnr":int, "rec_id":int, "qty":int, "epreis":decimal, "net_bet":decimal, "tax":decimal, "service":decimal, "bill_date":date, "betrag":decimal})
    summary_bill_list, Summary_bill = create_model("Summary_bill", {"subtotal":decimal, "total_service":decimal, "total_tax":decimal, "grand_total":decimal})

    Bill_guest = Guest
    Buff_hart = H_artikel
    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, summary_bill_list, lvcarea, fogl_date, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, compli_flag, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal bill_guest, buff_hart, h_art


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, ordered_item, summary_bill, bill_guest, buff_hart, h_art
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list, ordered_item_list, summary_bill_list
        return {"must_print": must_print, "rev_sign": rev_sign, "cancel_exist": cancel_exist, "price_decimal": price_decimal, "curr_local": curr_local, "curr_foreign": curr_foreign, "double_currency": double_currency, "foreign_rate": foreign_rate, "exchg_rate": exchg_rate, "f_disc": f_disc, "b_artnr": b_artnr, "b_title": b_title, "deptname": deptname, "curr_user": curr_user, "curr_waiter": curr_waiter, "tischnr": tischnr, "rechnr": rechnr, "pax": pax, "balance": balance, "balance_foreign": balance_foreign, "bcol": bcol, "printed": printed, "bill_date": bill_date, "kreditlimit": kreditlimit, "total_saldo": total_saldo, "msg_str": msg_str, "msg_str1": msg_str1, "rec_kellner": rec_kellner, "rec_bill_guest": rec_bill_guest, "cashless_flag": cashless_flag, "cashless_artnr": cashless_artnr, "multi_cash": multi_cash, "t-b-list": t_b_list_list, "t-h-bill": t_h_bill_list, "t-h-artikel": t_h_artikel_list, "summary-bill": summary_bill_list}

    def determine_revsign():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, summary_bill_list, lvcarea, fogl_date, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, compli_flag, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal bill_guest, buff_hart, h_art


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, ordered_item, summary_bill, bill_guest, buff_hart, h_art
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list, ordered_item_list, summary_bill_list

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

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, summary_bill_list, lvcarea, fogl_date, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, compli_flag, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal bill_guest, buff_hart, h_art


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, ordered_item, summary_bill, bill_guest, buff_hart, h_art
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list, ordered_item_list, summary_bill_list


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

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, summary_bill_list, lvcarea, fogl_date, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, compli_flag, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal bill_guest, buff_hart, h_art


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, ordered_item, summary_bill, bill_guest, buff_hart, h_art
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list, ordered_item_list, summary_bill_list

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

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, summary_bill_list, lvcarea, fogl_date, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, compli_flag, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal bill_guest, buff_hart, h_art


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, ordered_item, summary_bill, bill_guest, buff_hart, h_art
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list, ordered_item_list, summary_bill_list

        if double_currency:

            for b_list in query(b_list_list, filters=(lambda b_list :b_list.rechnr == h_bill.rechnr and b_list.departement == curr_dept)):
                t_b_list = T_b_list()
                t_b_list_list.append(t_b_list)

                buffer_copy(b_list, t_b_list)
                ordered_item = Ordered_item()
                ordered_item_list.append(ordered_item)

                ordered_item.dept = b_list.departement
                ordered_item.artnr = b_list.artnr
                ordered_item.rec_id = b_list._recid
                ordered_item.qty = b_list.anzahl
                ordered_item.epreis = b_list.epreis
                ordered_item.net_bet = b_list.nettobetrag
                ordered_item.bill_date = b_list.bill_datum
                ordered_item.betrag = b_list.betrag

        else:

            for b_list in query(b_list_list, filters=(lambda b_list :b_list.rechnr == h_bill.rechnr and b_list.departement == curr_dept)):
                t_b_list = T_b_list()
                t_b_list_list.append(t_b_list)

                buffer_copy(b_list, t_b_list)
                ordered_item = Ordered_item()
                ordered_item_list.append(ordered_item)

                ordered_item.dept = b_list.departement
                ordered_item.artnr = b_list.artnr
                ordered_item.rec_id = b_list._recid
                ordered_item.qty = b_list.anzahl
                ordered_item.epreis = b_list.epreis
                ordered_item.net_bet = b_list.nettobetrag
                ordered_item.bill_date = b_list.bill_datum
                ordered_item.betrag = b_list.betrag


    def cal_total_saldo():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, t_b_list_list, t_h_bill_list, t_h_artikel_list, summary_bill_list, lvcarea, fogl_date, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, compli_flag, h_bill_line, h_bill, h_artikel, guest, htparam, queasy, waehrung, artikel, hoteldpt, kellner, tisch, exrate
        nonlocal bill_guest, buff_hart, h_art


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, ordered_item, summary_bill, bill_guest, buff_hart, h_art
        nonlocal b_list_list, t_b_list_list, t_h_bill_list, t_h_artikel_list, ordered_item_list, summary_bill_list


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
            (Htparam.paramnr == 557)).first()

    if htparam.finteger != 0:
        f_discart = htparam.finteger

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

    if hoteldpt:
        servtax_use_foart = hoteldpt.defult

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 468)).first()

    if htparam:
        serv_disc = htparam.flogic

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 469)).first()

    if htparam:
        vat_disc = htparam.flogic

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 135)).first()
    incl_service = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 134)).first()
    incl_mwst = htparam.flogical
    serv_vat = get_output(htplogic(479))
    tax_vat = get_output(htplogic(483))

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

    for ordered_item in query(ordered_item_list):
        t_h_service = 0
        t_h_mwst = 0
        t_h_mwst2 = 0
        h_service = 0
        h_mwst = 0
        service = 0
        mwst = 0

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.departement == ordered_item.dept) &  (H_artikel.artnr == ordered_item.artnr) &  (H_artikel.artart == 0)).first()

        if h_artikel:
            netto_bet = netto_bet + (ordered_item.epreis * ordered_item.qty)

            if not servtax_use_foart:
                serv_code = h_artikel.service_code
                vat_code = h_artikel.mwst_code


            else:

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()

                if artikel:
                    serv_code = artikel.service_code
                    vat_code = artikel.mwst_code

        if h_artikel:

            if ordered_item.artnr != f_discart:

                if serv_code != 0 and not incl_service:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == serv_code)).first()

                    if htparam and htparam.fdecimal != 0:

                        if num_entries(htparam.fchar, chr(2)) >= 2:
                            t_h_service = decimal.Decimal(entry(1, htparam.fchar, chr(2))) / 10000


                        else:
                            t_h_service = htparam.fdecimal

                if vat_code != 0 and not incl_mwst:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == vat_code)).first()

                    if htparam and htparam.fdecimal != 0:

                        if num_entries(htparam.fchar, chr(2)) >= 2:
                            t_h_mwst = decimal.Decimal(entry(1, htparam.fchar, chr(2))) / 10000


                        else:
                            t_h_mwst = htparam.fdecimal

                        if serv_vat and not tax_vat:
                            t_h_mwst = t_h_mwst + t_h_mwst * t_h_service / 100

                        elif serv_vat and tax_vat:
                            t_h_mwst = t_h_mwst + t_h_mwst * (t_h_service + t_h_mwst2) / 100

                        elif not serv_vat and tax_vat:
                            t_h_mwst = t_h_mwst + t_h_mwst * t_h_mwst2 / 100
                        ct = replace_str(to_string(t_h_mwst) , ".", ",")
                        l_deci = len(entry(1, ct, ","))

                        if l_deci <= 2:
                            t_h_mwst = round(t_h_mwst, 2)

                        elif l_deci == 3:
                            t_h_mwst = round(t_h_mwst, 3)
                        else:
                            t_h_mwst = round(t_h_mwst, 4)

                if t_h_service != 0 or t_h_mwst != 0:
                    t_h_service = t_h_service / 100
                    t_h_mwst = t_h_mwst / 100
                    t_h_mwst2 = t_h_mwst2 / 100


                    fact_scvat = 1 + t_h_service + t_h_mwst + t_h_mwst2
                    h_service = ordered_item.betrag / fact_scvat * t_h_service
                    h_service = round(h_service, 2)
                    h_mwst = ordered_item.betrag / fact_scvat * t_h_mwst
                    h_mwst = round(h_mwst, 2)

                    if not incl_service:
                        service = service + h_service

                    if not incl_mwst:
                        mwst = mwst + h_mwst
                        mwst1 = mwst1 + h_mwst
            else:

                if serv_code != 0 and not incl_service and serv_disc:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == serv_code)).first()

                    if htparam and htparam.fdecimal != 0:

                        if num_entries(htparam.fchar, chr(2)) >= 2:
                            t_h_service = decimal.Decimal(entry(1, htparam.fchar, chr(2))) / 10000


                        else:
                            t_h_service = htparam.fdecimal

                if vat_code != 0 and not incl_mwst and vat_disc:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == vat_code)).first()

                    if htparam and htparam.fdecimal != 0:

                        if num_entries(htparam.fchar, chr(2)) >= 2:
                            t_h_mwst = decimal.Decimal(entry(1, htparam.fchar, chr(2))) / 10000


                        else:
                            t_h_mwst = htparam.fdecimal

                        if serv_vat and not tax_vat:
                            t_h_mwst = t_h_mwst + t_h_mwst * t_h_service / 100

                        elif serv_vat and tax_vat:
                            t_h_mwst = t_h_mwst + t_h_mwst * (t_h_service + t_h_mwst2) / 100

                        elif not serv_vat and tax_vat:
                            t_h_mwst = t_h_mwst + t_h_mwst * t_h_mwst2 / 100
                        ct = replace_str(to_string(t_h_mwst) , ".", ",")
                        l_deci = len(entry(1, ct, ","))

                        if l_deci <= 2:
                            t_h_mwst = round(t_h_mwst, 2)

                        elif l_deci == 3:
                            t_h_mwst = round(t_h_mwst, 3)
                        else:
                            t_h_mwst = round(t_h_mwst, 4)

                if ordered_item.epreis != ordered_item.betrag:

                    if t_h_service != 0 or t_h_mwst != 0:
                        t_h_service = t_h_service / 100
                        t_h_mwst = t_h_mwst / 100
                        t_h_mwst2 = t_h_mwst2 / 100


                        fact_scvat = 1 + t_h_service + t_h_mwst + t_h_mwst2
                        h_service = ordered_item.betrag / fact_scvat * t_h_service
                        h_service = round(h_service, 2)
                        h_mwst = ordered_item.betrag / fact_scvat * t_h_mwst
                        h_mwst = round(h_mwst, 2)

                        if not incl_service:
                            service = service + h_service

                        if not incl_mwst:
                            mwst = mwst + h_mwst
                            mwst1 = mwst1 + h_mwst
            ordered_item.service = service
            ordered_item.tax = mwst

    for ordered_item in query(ordered_item_list):
        buff_hart = db_session.query(Buff_hart).filter((Buff_hart.artnr == ordered_item.artnr) &  (Buff_hart.departement == ordered_item.dept)).first()
        if not buff_hart:
            continue

        sub_tot = netto_bet
        tot_serv = tot_serv + ordered_item.service
        tot_tax = tot_tax + ordered_item.tax

        if buff_hart.artart == 11 or buff_hart.artart == 12:
            compli_flag = True

    if compli_flag:
        tot_serv = 0
        tot_tax = 0
    grand_tot = sub_tot + tot_serv + tot_tax
    summary_bill = Summary_bill()
    summary_bill_list.append(summary_bill)

    summary_bill.subtotal = sub_tot
    summary_bill.total_service = tot_serv
    summary_bill.total_tax = tot_tax
    summary_bill.grand_total = grand_tot

    return generate_output()