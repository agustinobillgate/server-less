#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.calc_servtaxesbl import calc_servtaxesbl
from models import H_bill_line, H_bill, H_artikel, Guest, Artikel, Htparam, Queasy, Waehrung, Hoteldpt, Kellner, Tisch, Exrate

def prepare_ts_closeinv_2_webbl(pvilanguage:int, curr_dept:int, inp_rechnr:int, user_init:string, user_name:string, curr_printer:int):

    prepare_cache ([H_bill_line, H_artikel, Guest, Artikel, Htparam, Waehrung, Hoteldpt, Kellner, Tisch, Exrate])

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
    o_disc = 0
    t_b_list_data = []
    t_h_bill_data = []
    t_h_artikel_data = []
    t_h_artsales_data = []
    summary_bill_data = []
    lvcarea:string = "TS-closeinv"
    fogl_date:date = None
    t_serv_perc:Decimal = to_decimal("0.0")
    t_mwst_perc:Decimal = to_decimal("0.0")
    t_fact:Decimal = 1
    t_service:Decimal = to_decimal("0.0")
    t_mwst1:Decimal = to_decimal("0.0")
    t_mwst:Decimal = to_decimal("0.0")
    h_service:Decimal = to_decimal("0.0")
    h_mwst:Decimal = to_decimal("0.0")
    h_mwst2:Decimal = to_decimal("0.0")
    t_h_service:Decimal = to_decimal("0.0")
    t_h_mwst:Decimal = to_decimal("0.0")
    t_h_mwst2:Decimal = to_decimal("0.0")
    incl_service:bool = False
    incl_mwst:bool = False
    gst_logic:bool = False
    serv_disc:bool = True
    vat_disc:bool = True
    f_discart:int = -1
    amount:Decimal = to_decimal("0.0")
    f_dec:Decimal = to_decimal("0.0")
    serv_code:int = 0
    vat_code:int = 0
    servtax_use_foart:bool = False
    serv_vat:bool = False
    tax_vat:bool = False
    ct:string = ""
    l_deci:int = 2
    fact_scvat:Decimal = 1
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    mwst:Decimal = to_decimal("0.0")
    mwst1:Decimal = to_decimal("0.0")
    sub_tot:Decimal = to_decimal("0.0")
    tot_serv:Decimal = to_decimal("0.0")
    tot_tax:Decimal = to_decimal("0.0")
    grand_tot:Decimal = to_decimal("0.0")
    netto_bet:Decimal = to_decimal("0.0")
    compli_flag:bool = False
    serv_perc:Decimal = to_decimal("0.0")
    vat_perc:Decimal = to_decimal("0.0")
    vat2_perc:Decimal = to_decimal("0.0")
    servat_perc:Decimal = to_decimal("0.0")
    h_bill_line = h_bill = h_artikel = guest = artikel = htparam = queasy = waehrung = hoteldpt = kellner = tisch = exrate = None

    b_list = t_b_list = t_h_bill = t_h_artikel = t_h_artsales = ordered_item = summary_bill = bill_guest = buff_hart = abuff = None

    b_list_data, B_list = create_model_like(H_bill_line, {"rec_id":int})
    t_b_list_data, T_b_list = create_model_like(H_bill_line, {"rec_id":int, "t_time":string})
    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_h_artikel_data, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})
    t_h_artsales_data, T_h_artsales = create_model_like(H_artikel, {"rec_id":int})
    ordered_item_data, Ordered_item = create_model("Ordered_item", {"dept":int, "artnr":int, "rec_id":int, "qty":int, "epreis":Decimal, "net_bet":Decimal, "tax":Decimal, "service":Decimal, "bill_date":date, "betrag":Decimal})
    summary_bill_data, Summary_bill = create_model("Summary_bill", {"subtotal":Decimal, "total_service":Decimal, "total_tax":Decimal, "grand_total":Decimal})

    Bill_guest = create_buffer("Bill_guest",Guest)
    Buff_hart = create_buffer("Buff_hart",H_artikel)
    Abuff = create_buffer("Abuff",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, o_disc, t_b_list_data, t_h_bill_data, t_h_artikel_data, t_h_artsales_data, summary_bill_data, lvcarea, fogl_date, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, compli_flag, serv_perc, vat_perc, vat2_perc, servat_perc, h_bill_line, h_bill, h_artikel, guest, artikel, htparam, queasy, waehrung, hoteldpt, kellner, tisch, exrate
        nonlocal pvilanguage, curr_dept, inp_rechnr, user_init, user_name, curr_printer
        nonlocal bill_guest, buff_hart, abuff


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, t_h_artsales, ordered_item, summary_bill, bill_guest, buff_hart, abuff
        nonlocal b_list_data, t_b_list_data, t_h_bill_data, t_h_artikel_data, t_h_artsales_data, ordered_item_data, summary_bill_data

        return {"must_print": must_print, "rev_sign": rev_sign, "cancel_exist": cancel_exist, "price_decimal": price_decimal, "curr_local": curr_local, "curr_foreign": curr_foreign, "double_currency": double_currency, "foreign_rate": foreign_rate, "exchg_rate": exchg_rate, "f_disc": f_disc, "b_artnr": b_artnr, "b_title": b_title, "deptname": deptname, "curr_user": curr_user, "curr_waiter": curr_waiter, "tischnr": tischnr, "rechnr": rechnr, "pax": pax, "balance": balance, "balance_foreign": balance_foreign, "bcol": bcol, "printed": printed, "bill_date": bill_date, "kreditlimit": kreditlimit, "total_saldo": total_saldo, "msg_str": msg_str, "msg_str1": msg_str1, "rec_kellner": rec_kellner, "rec_bill_guest": rec_bill_guest, "cashless_flag": cashless_flag, "cashless_artnr": cashless_artnr, "multi_cash": multi_cash, "o_disc": o_disc, "t-b-list": t_b_list_data, "t-h-bill": t_h_bill_data, "t-h-artikel": t_h_artikel_data, "t-h-artsales": t_h_artsales_data, "summary-bill": summary_bill_data}

    def determine_revsign():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, o_disc, t_b_list_data, t_h_bill_data, t_h_artikel_data, t_h_artsales_data, summary_bill_data, lvcarea, fogl_date, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, compli_flag, serv_perc, vat_perc, vat2_perc, servat_perc, h_bill_line, h_bill, h_artikel, guest, artikel, htparam, queasy, waehrung, hoteldpt, kellner, tisch, exrate
        nonlocal pvilanguage, curr_dept, inp_rechnr, user_init, user_name, curr_printer
        nonlocal bill_guest, buff_hart, abuff


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, t_h_artsales, ordered_item, summary_bill, bill_guest, buff_hart, abuff
        nonlocal b_list_data, t_b_list_data, t_h_bill_data, t_h_artikel_data, t_h_artsales_data, ordered_item_data, summary_bill_data

        s:Decimal = to_decimal("0.0")

        h_bill_line_obj_list = {}
        h_bill_line = H_bill_line()
        h_artikel = H_artikel()
        for h_bill_line.betrag, h_bill_line.artnr, h_bill_line.departement, h_bill_line.bill_datum, h_bill_line.bezeich, h_bill_line.anzahl, h_bill_line.nettobetrag, h_bill_line.fremdwbetrag, h_bill_line.tischnr, h_bill_line.epreis, h_bill_line.zeit, h_bill_line.sysdate, h_bill_line.segmentcode, h_bill_line.waehrungsnr, h_bill_line._recid, h_artikel.artnrfront, h_artikel.departement, h_artikel.artart, h_artikel._recid in db_session.query(H_bill_line.betrag, H_bill_line.artnr, H_bill_line.departement, H_bill_line.bill_datum, H_bill_line.bezeich, H_bill_line.anzahl, H_bill_line.nettobetrag, H_bill_line.fremdwbetrag, H_bill_line.tischnr, H_bill_line.epreis, H_bill_line.zeit, H_bill_line.sysdate, H_bill_line.segmentcode, H_bill_line.waehrungsnr, H_bill_line._recid, H_artikel.artnrfront, H_artikel.departement, H_artikel.artart, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                 (H_bill_line.rechnr == inp_rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line._recid).all():
            if h_bill_line_obj_list.get(h_bill_line._recid):
                continue
            else:
                h_bill_line_obj_list[h_bill_line._recid] = True


            s =  to_decimal(s) + to_decimal(h_bill_line.betrag)

        if s < 0:
            rev_sign = - 1


    def open_table():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, o_disc, t_b_list_data, t_h_bill_data, t_h_artikel_data, t_h_artsales_data, summary_bill_data, lvcarea, fogl_date, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, compli_flag, serv_perc, vat_perc, vat2_perc, servat_perc, h_bill_line, h_bill, h_artikel, guest, artikel, htparam, queasy, waehrung, hoteldpt, kellner, tisch, exrate
        nonlocal pvilanguage, curr_dept, inp_rechnr, user_init, user_name, curr_printer
        nonlocal bill_guest, buff_hart, abuff


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, t_h_artsales, ordered_item, summary_bill, bill_guest, buff_hart, abuff
        nonlocal b_list_data, t_b_list_data, t_h_bill_data, t_h_artikel_data, t_h_artsales_data, ordered_item_data, summary_bill_data


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

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, o_disc, t_b_list_data, t_h_bill_data, t_h_artikel_data, t_h_artsales_data, summary_bill_data, lvcarea, fogl_date, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, compli_flag, serv_perc, vat_perc, vat2_perc, servat_perc, h_bill_line, h_bill, h_artikel, guest, artikel, htparam, queasy, waehrung, hoteldpt, kellner, tisch, exrate
        nonlocal pvilanguage, curr_dept, inp_rechnr, user_init, user_name, curr_printer
        nonlocal bill_guest, buff_hart, abuff


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, t_h_artsales, ordered_item, summary_bill, bill_guest, buff_hart, abuff
        nonlocal b_list_data, t_b_list_data, t_h_bill_data, t_h_artikel_data, t_h_artsales_data, ordered_item_data, summary_bill_data

        h_art = None
        create_it:bool = False
        H_art =  create_buffer("H_art",H_artikel)

        for h_bill_line in db_session.query(H_bill_line).filter(
                 (H_bill_line.rechnr == inp_rechnr) & (H_bill_line.departement == curr_dept)).order_by(H_bill_line.waehrungsnr).all():
            create_it = True

            h_art = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"departement": [(eq, h_bill_line.departement)]})

            if (h_art and h_art.artart != 0) or h_bill_line.artnr == 0:

                b_list = query(b_list_data, filters=(lambda b_list: b_list.artnr == h_bill_line.artnr and b_list.betrag == - h_bill_line.betrag and b_list.bill_datum == h_bill_line.bill_datum), first=True)

                if b_list:
                    b_list_data.remove(b_list)
                    create_it = False
                else:
                    bill_date = h_bill_line.bill_datum

            if create_it:
                b_list = B_list()
                b_list_data.append(b_list)

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
                b_list.rec_id = h_bill_line._recid

        if htparam.fdate != bill_date and double_currency:

            exrate = get_cache (Exrate, {"datum": [(eq, bill_date)]})

            if exrate:
                exchg_rate =  to_decimal(exrate.betrag)


    def disp_bill_line():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, o_disc, t_b_list_data, t_h_bill_data, t_h_artikel_data, t_h_artsales_data, summary_bill_data, lvcarea, fogl_date, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, compli_flag, serv_perc, vat_perc, vat2_perc, servat_perc, h_bill_line, h_bill, h_artikel, guest, artikel, htparam, queasy, waehrung, hoteldpt, kellner, tisch, exrate
        nonlocal pvilanguage, curr_dept, inp_rechnr, user_init, user_name, curr_printer
        nonlocal bill_guest, buff_hart, abuff


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, t_h_artsales, ordered_item, summary_bill, bill_guest, buff_hart, abuff
        nonlocal b_list_data, t_b_list_data, t_h_bill_data, t_h_artikel_data, t_h_artsales_data, ordered_item_data, summary_bill_data

        if double_currency:

            for b_list in query(b_list_data, filters=(lambda b_list: b_list.rechnr == h_bill.rechnr and b_list.departement == curr_dept), sort_by=[("sysdate",True),("zeit",True)]):
                t_b_list = T_b_list()
                t_b_list_data.append(t_b_list)

                buffer_copy(b_list, t_b_list)
                t_b_list.t_time = to_string(b_list.zeit, "HH:MM:SS")


                ordered_item = Ordered_item()
                ordered_item_data.append(ordered_item)

                ordered_item.dept = b_list.departement
                ordered_item.artnr = b_list.artnr
                ordered_item.rec_id = b_list._recid
                ordered_item.qty = b_list.anzahl
                ordered_item.epreis =  to_decimal(b_list.epreis)
                ordered_item.net_bet =  to_decimal(b_list.nettobetrag)
                ordered_item.bill_date = b_list.bill_datum
                ordered_item.betrag =  to_decimal(b_list.betrag)

        else:

            for b_list in query(b_list_data, filters=(lambda b_list: b_list.rechnr == h_bill.rechnr and b_list.departement == curr_dept), sort_by=[("sysdate",True),("zeit",True)]):
                t_b_list = T_b_list()
                t_b_list_data.append(t_b_list)

                buffer_copy(b_list, t_b_list)
                t_b_list.t_time = to_string(b_list.zeit, "HH:MM:SS")


                ordered_item = Ordered_item()
                ordered_item_data.append(ordered_item)

                ordered_item.dept = b_list.departement
                ordered_item.artnr = b_list.artnr
                ordered_item.rec_id = b_list._recid
                ordered_item.qty = b_list.anzahl
                ordered_item.epreis =  to_decimal(b_list.epreis)
                ordered_item.net_bet =  to_decimal(b_list.nettobetrag)
                ordered_item.bill_date = b_list.bill_datum
                ordered_item.betrag =  to_decimal(b_list.betrag)

    def cal_total_saldo():

        nonlocal must_print, rev_sign, cancel_exist, price_decimal, curr_local, curr_foreign, double_currency, foreign_rate, exchg_rate, f_disc, b_artnr, b_title, deptname, curr_user, curr_waiter, tischnr, rechnr, pax, balance, balance_foreign, bcol, printed, bill_date, kreditlimit, total_saldo, msg_str, msg_str1, rec_kellner, rec_bill_guest, cashless_flag, cashless_artnr, multi_cash, o_disc, t_b_list_data, t_h_bill_data, t_h_artikel_data, t_h_artsales_data, summary_bill_data, lvcarea, fogl_date, t_serv_perc, t_mwst_perc, t_fact, t_service, t_mwst1, t_mwst, h_service, h_mwst, h_mwst2, t_h_service, t_h_mwst, t_h_mwst2, incl_service, incl_mwst, gst_logic, serv_disc, vat_disc, f_discart, amount, f_dec, serv_code, vat_code, servtax_use_foart, serv_vat, tax_vat, ct, l_deci, fact_scvat, service, vat, vat2, mwst, mwst1, sub_tot, tot_serv, tot_tax, grand_tot, netto_bet, compli_flag, serv_perc, vat_perc, vat2_perc, servat_perc, h_bill_line, h_bill, h_artikel, guest, artikel, htparam, queasy, waehrung, hoteldpt, kellner, tisch, exrate
        nonlocal pvilanguage, curr_dept, inp_rechnr, user_init, user_name, curr_printer
        nonlocal bill_guest, buff_hart, abuff


        nonlocal b_list, t_b_list, t_h_bill, t_h_artikel, t_h_artsales, ordered_item, summary_bill, bill_guest, buff_hart, abuff
        nonlocal b_list_data, t_b_list_data, t_h_bill_data, t_h_artikel_data, t_h_artsales_data, ordered_item_data, summary_bill_data


        total_saldo =  to_decimal("0")

        h_bill = get_cache (H_bill, {"rechnr": [(eq, inp_rechnr)],"departement": [(eq, curr_dept)]})

        if h_bill:

            h_bill_line_obj_list = {}
            h_bill_line = H_bill_line()
            h_artikel = H_artikel()
            for h_bill_line.betrag, h_bill_line.artnr, h_bill_line.departement, h_bill_line.bill_datum, h_bill_line.bezeich, h_bill_line.anzahl, h_bill_line.nettobetrag, h_bill_line.fremdwbetrag, h_bill_line.tischnr, h_bill_line.epreis, h_bill_line.zeit, h_bill_line.sysdate, h_bill_line.segmentcode, h_bill_line.waehrungsnr, h_bill_line._recid, h_artikel.artnrfront, h_artikel.departement, h_artikel.artart, h_artikel._recid in db_session.query(H_bill_line.betrag, H_bill_line.artnr, H_bill_line.departement, H_bill_line.bill_datum, H_bill_line.bezeich, H_bill_line.anzahl, H_bill_line.nettobetrag, H_bill_line.fremdwbetrag, H_bill_line.tischnr, H_bill_line.epreis, H_bill_line.zeit, H_bill_line.sysdate, H_bill_line.segmentcode, H_bill_line.waehrungsnr, H_bill_line._recid, H_artikel.artnrfront, H_artikel.departement, H_artikel.artart, H_artikel._recid).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement) & (H_artikel.artart == 0)).filter(
                     (H_bill_line.rechnr == inp_rechnr) & (H_bill_line.departement == h_bill.departement) & (H_bill_line.artnr != 0)).order_by(H_bill_line._recid).all():
                if h_bill_line_obj_list.get(h_bill_line._recid):
                    continue
                else:
                    h_bill_line_obj_list[h_bill_line._recid] = True


                total_saldo =  to_decimal(total_saldo) + to_decimal(h_bill_line.betrag)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

    if htparam.finteger != 0:
        f_discart = htparam.finteger

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
    b_artnr = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 556)]})
    o_disc = htparam.finteger

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

    if hoteldpt:
        servtax_use_foart = hoteldpt.defult

    htparam = get_cache (Htparam, {"paramnr": [(eq, 468)]})

    if htparam:
        serv_disc = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 469)]})

    if htparam:
        vat_disc = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 135)]})
    incl_service = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 134)]})
    incl_mwst = htparam.flogical
    serv_vat = get_output(htplogic(479))
    tax_vat = get_output(htplogic(483))

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
        t_h_bill_data.append(t_h_bill)

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
        t_h_artikel_data.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = to_int(h_artikel._recid)

        if t_h_artikel.artnr == cashless_artnr:
            t_h_artikel.bezeich = replace_str(t_h_artikel.bezeich, " ", "")

    if bill_guest:
        rec_bill_guest = bill_guest._recid

    for h_artikel in db_session.query(H_artikel).filter(
             (H_artikel.departement == curr_dept) & (H_artikel.artart == 0)).order_by(H_artikel._recid).all():
        t_h_artsales = T_h_artsales()
        t_h_artsales_data.append(t_h_artsales)

        buffer_copy(h_artikel, t_h_artsales)
        t_h_artsales.rec_id = to_int(h_artikel._recid)

    for ordered_item in query(ordered_item_data):
        t_h_service =  to_decimal("0")
        t_h_mwst =  to_decimal("0")
        t_h_mwst2 =  to_decimal("0")
        h_service =  to_decimal("0")
        h_mwst =  to_decimal("0")
        service =  to_decimal("0")
        mwst =  to_decimal("0")

        if ordered_item.bill_date < bill_date:

            buff_hart = get_cache (H_artikel, {"artnr": [(eq, ordered_item.artnr)],"departement": [(eq, ordered_item.dept)]})

            abuff = get_cache (Artikel, {"artnr": [(eq, buff_hart.artnrfront)],"departement": [(eq, buff_hart.departement)]})
            serv_perc, vat_perc, vat2_perc, servat_perc = get_output(calc_servtaxesbl(1, abuff.artnr, abuff.departement, ordered_item.bill_date))
            ordered_item.service =  to_decimal(serv_perc)
            ordered_item.tax =  to_decimal(vat_perc) + to_decimal(vat2_perc)
        else:

            h_artikel = get_cache (H_artikel, {"departement": [(eq, ordered_item.dept)],"artnr": [(eq, ordered_item.artnr)],"artart": [(eq, 0)]})

            if h_artikel:
                netto_bet =  to_decimal(netto_bet) + to_decimal((ordered_item.epreis) * to_decimal(ordered_item.qty))

                if not servtax_use_foart:
                    serv_code = h_artikel.service_code
                    vat_code = h_artikel.mwst_code


                else:

                    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                    if artikel:
                        serv_code = artikel.service_code
                        vat_code = artikel.mwst_code

            if h_artikel:

                if ordered_item.artnr != f_discart:

                    if serv_code != 0 and not incl_service:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, serv_code)]})

                        if htparam and htparam.fdecimal != 0:

                            if num_entries(htparam.fchar, chr_unicode(2)) >= 2:
                                t_h_service =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")


                            else:
                                t_h_service =  to_decimal(htparam.fdecimal)

                    if vat_code != 0 and not incl_mwst:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, vat_code)]})

                        if htparam and htparam.fdecimal != 0:

                            if num_entries(htparam.fchar, chr_unicode(2)) >= 2:
                                t_h_mwst =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")


                            else:
                                t_h_mwst =  to_decimal(htparam.fdecimal)

                            if serv_vat and not tax_vat:
                                t_h_mwst =  to_decimal(t_h_mwst) + to_decimal(t_h_mwst) * to_decimal(t_h_service) / to_decimal("100")

                            elif serv_vat and tax_vat:
                                t_h_mwst =  to_decimal(t_h_mwst) + to_decimal(t_h_mwst) * to_decimal((t_h_service) + to_decimal(t_h_mwst2)) / to_decimal("100")

                            elif not serv_vat and tax_vat:
                                t_h_mwst =  to_decimal(t_h_mwst) + to_decimal(t_h_mwst) * to_decimal(t_h_mwst2) / to_decimal("100")
                            ct = replace_str(to_string(t_h_mwst) , ".", ",")
                            l_deci = length(entry(1, ct, ","))

                            if l_deci <= 2:
                                t_h_mwst = to_decimal(round(t_h_mwst , 2))

                            elif l_deci == 3:
                                t_h_mwst = to_decimal(round(t_h_mwst , 3))
                            else:
                                t_h_mwst = to_decimal(round(t_h_mwst , 4))

                    if t_h_service != 0 or t_h_mwst != 0:
                        t_h_service =  to_decimal(t_h_service) / to_decimal("100")
                        t_h_mwst =  to_decimal(t_h_mwst) / to_decimal("100")
                        t_h_mwst2 =  to_decimal(t_h_mwst2) / to_decimal("100")


                        fact_scvat =  to_decimal("1") + to_decimal(t_h_service) + to_decimal(t_h_mwst) + to_decimal(t_h_mwst2)
                        h_service =  to_decimal(ordered_item.betrag) / to_decimal(fact_scvat) * to_decimal(t_h_service)
                        h_service = to_decimal(round(h_service , 2))
                        h_mwst =  to_decimal(ordered_item.betrag) / to_decimal(fact_scvat) * to_decimal(t_h_mwst)
                        h_mwst = to_decimal(round(h_mwst , 2))

                        if not incl_service:
                            service =  to_decimal(service) + to_decimal(h_service)

                        if not incl_mwst:
                            mwst =  to_decimal(mwst) + to_decimal(h_mwst)
                            mwst1 =  to_decimal(mwst1) + to_decimal(h_mwst)
                else:

                    if serv_code != 0 and not incl_service and serv_disc:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, serv_code)]})

                        if htparam and htparam.fdecimal != 0:

                            if num_entries(htparam.fchar, chr_unicode(2)) >= 2:
                                t_h_service =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")


                            else:
                                t_h_service =  to_decimal(htparam.fdecimal)

                    if vat_code != 0 and not incl_mwst and vat_disc:

                        htparam = get_cache (Htparam, {"paramnr": [(eq, vat_code)]})

                        if htparam and htparam.fdecimal != 0:

                            if num_entries(htparam.fchar, chr_unicode(2)) >= 2:
                                t_h_mwst =  to_decimal(to_decimal(entry(1 , htparam.fchar , chr_unicode(2)))) / to_decimal("10000")


                            else:
                                t_h_mwst =  to_decimal(htparam.fdecimal)

                            if serv_vat and not tax_vat:
                                t_h_mwst =  to_decimal(t_h_mwst) + to_decimal(t_h_mwst) * to_decimal(t_h_service) / to_decimal("100")

                            elif serv_vat and tax_vat:
                                t_h_mwst =  to_decimal(t_h_mwst) + to_decimal(t_h_mwst) * to_decimal((t_h_service) + to_decimal(t_h_mwst2)) / to_decimal("100")

                            elif not serv_vat and tax_vat:
                                t_h_mwst =  to_decimal(t_h_mwst) + to_decimal(t_h_mwst) * to_decimal(t_h_mwst2) / to_decimal("100")
                            ct = replace_str(to_string(t_h_mwst) , ".", ",")
                            l_deci = length(entry(1, ct, ","))

                            if l_deci <= 2:
                                t_h_mwst = to_decimal(round(t_h_mwst , 2))

                            elif l_deci == 3:
                                t_h_mwst = to_decimal(round(t_h_mwst , 3))
                            else:
                                t_h_mwst = to_decimal(round(t_h_mwst , 4))

                    if ordered_item.epreis != ordered_item.betrag:

                        if t_h_service != 0 or t_h_mwst != 0:
                            t_h_service =  to_decimal(t_h_service) / to_decimal("100")
                            t_h_mwst =  to_decimal(t_h_mwst) / to_decimal("100")
                            t_h_mwst2 =  to_decimal(t_h_mwst2) / to_decimal("100")


                            fact_scvat =  to_decimal("1") + to_decimal(t_h_service) + to_decimal(t_h_mwst) + to_decimal(t_h_mwst2)
                            h_service =  to_decimal(ordered_item.betrag) / to_decimal(fact_scvat) * to_decimal(t_h_service)
                            h_service = to_decimal(round(h_service , 2))
                            h_mwst =  to_decimal(ordered_item.betrag) / to_decimal(fact_scvat) * to_decimal(t_h_mwst)
                            h_mwst = to_decimal(round(h_mwst , 2))

                            if not incl_service:
                                service =  to_decimal(service) + to_decimal(h_service)

                            if not incl_mwst:
                                mwst =  to_decimal(mwst) + to_decimal(h_mwst)
                                mwst1 =  to_decimal(mwst1) + to_decimal(h_mwst)
                ordered_item.service =  to_decimal(service)
                ordered_item.tax =  to_decimal(mwst)

    buff_hart_obj_list = {}
    for buff_hart in db_session.query(Buff_hart).filter(
             ((Buff_hart.artnr.in_(list(set([ordered_item.artnr for ordered_item in ordered_item_data])))) & (Buff_hart.departement == ordered_item.dept))).order_by(Buff_hart._recid).all():
        if buff_hart_obj_list.get(buff_hart._recid):
            continue
        else:
            buff_hart_obj_list[buff_hart._recid] = True


        sub_tot =  to_decimal(netto_bet)
        tot_serv =  to_decimal(tot_serv) + to_decimal(ordered_item.service)
        tot_tax =  to_decimal(tot_tax) + to_decimal(ordered_item.tax)

        if buff_hart.artart == 11 or buff_hart.artart == 12:
            compli_flag = True

    if compli_flag:
        tot_serv =  to_decimal("0")
        tot_tax =  to_decimal("0")
    grand_tot =  to_decimal(sub_tot) + to_decimal(tot_serv) + to_decimal(tot_tax)
    summary_bill = Summary_bill()
    summary_bill_data.append(summary_bill)

    summary_bill.subtotal =  to_decimal(sub_tot)
    summary_bill.total_service =  to_decimal(tot_serv)
    summary_bill.total_tax =  to_decimal(tot_tax)
    summary_bill.grand_total = to_decimal(round(grand_tot , price_decimal))

    return generate_output()