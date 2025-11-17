# using conversion tools version: 1.0.0.119
"""_yusufwijasena_17/11/2025

    Ticket ID: 20FD2B
        remark: - fix python indentation 
"""
from functions.additional_functions import *
from decimal import Decimal
from functions.ts_splitbill_build_lmenubl import ts_splitbill_build_lmenubl
from models import H_bill, H_bill_line, H_artikel, Htparam, Waehrung, Hoteldpt, H_mjourn


def prepare_ts_splitbill_webbl(dept: int, tischnr: int):

    prepare_cache([H_artikel, Htparam, Waehrung, Hoteldpt, H_mjourn])

    multi_vat = False
    zero_flag = False
    multi_cash = False
    price_decimal = 0
    foreign_rate = False
    double_currency = False
    exchg_rate = 1
    deptname = ""
    must_print = False
    fl_warn = False
    max_lapos = 0
    cashless_flag = False
    t_h_bill_data = []
    t_h_bill_line_data = []
    menu_data = []
    lhbline_data = []
    list_reqst: List[str] = create_empty_list(15, "")
    counter: int = 0
    nr: int = 0
    h_bill_line_recid: int = 0
    h_bill = h_bill_line = h_artikel = htparam = waehrung = hoteldpt = h_mjourn = None

    menu = lhbline = t_h_bill = t_h_bill_line = h_artikel_buff = None

    menu_data, Menu = create_model(
        "Menu",
        {
            "pos": int,
            "bezeich": str,
            "artnr": int
        })
    lhbline_data, Lhbline = create_model(
        "Lhbline",
        {
            "nr": int,
            "rid": int
        })
    t_h_bill_data, T_h_bill = create_model_like(
        H_bill,
        {
            "rec_id": int
        })
    t_h_bill_line_data, T_h_bill_line = create_model_like(
        H_bill_line,
        {
            "rec_id": int,
            "menu_flag": int,
            "sub_menu_bezeich": str,
            "sub_menu_betriebsnr": int,
            "sub_menu_qty": int
        })

    H_artikel_buff = create_buffer("H_artikel_buff", H_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal multi_vat, zero_flag, multi_cash, price_decimal, foreign_rate, double_currency, exchg_rate, deptname, must_print, fl_warn, max_lapos, cashless_flag, t_h_bill_data, t_h_bill_line_data, menu_data, lhbline_data, list_reqst, counter, nr, h_bill_line_recid, h_bill, h_bill_line, h_artikel, htparam, waehrung, hoteldpt, h_mjourn
        nonlocal dept, tischnr
        nonlocal h_artikel_buff
        nonlocal menu, lhbline, t_h_bill, t_h_bill_line, h_artikel_buff
        nonlocal menu_data, lhbline_data, t_h_bill_data, t_h_bill_line_data

        return {
            "multi_vat": multi_vat,
            "zero_flag": zero_flag,
            "multi_cash": multi_cash,
            "price_decimal": price_decimal,
            "foreign_rate": foreign_rate,
            "double_currency": double_currency,
            "exchg_rate": exchg_rate,
            "deptname": deptname,
            "must_print": must_print,
            "fl_warn": fl_warn,
            "max_lapos": max_lapos,
            "cashless_flag": cashless_flag,
            "t-h-bill": t_h_bill_data,
            "t-h-bill-line": t_h_bill_line_data,
            "menu": menu_data,
            "Lhbline": lhbline_data
        }

    htparam = get_cache(Htparam, {"paramnr": [(eq, 834)]})
    cashless_flag = htparam.flogical

    htparam = get_cache(Htparam, {"paramnr": [(eq, 271)]})

    if htparam.feldtyp == 4:
        multi_vat = htparam.flogical

    htparam = get_cache(Htparam, {"paramnr": [(eq, 869)]})
    zero_flag = htparam.flogical

    htparam = get_cache(Htparam, {"paramnr": [(eq, 833)]})
    multi_cash = htparam.flogical

    htparam = get_cache(Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache(Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache(Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    if foreign_rate:
        htparam = get_cache(Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache(Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate = to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    hoteldpt = get_cache(Hoteldpt, {"num": [(eq, dept)]})
    deptname = hoteldpt.depart

    htparam = get_cache(Htparam, {"paramnr": [(eq, 877)]})
    must_print = htparam.flogical

    h_bill = get_cache(
        H_bill, {"departement": [(eq, dept)], "tischnr": [(eq, tischnr)], "flag": [(eq, 0)]})

    if not h_bill:
        return generate_output()
    t_h_bill = T_h_bill()
    t_h_bill_data.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    htparam = get_cache(Htparam, {"paramnr": [(eq, 948)]})

    if htparam.paramgruppe == 19 and htparam.flogical:
        htparam = get_cache(Htparam, {"paramnr": [(eq, 557)]})

        h_bill_line = get_cache(
            H_bill_line, {"rechnr": [(eq, h_bill.rechnr)], "departement": [(eq, dept)], "artnr": [(eq, htparam.finteger)], "betrag": [(ne, 0)]})

        if h_bill_line:
            fl_warn = True

    h_bill_line_obj_list = {}
    for h_bill_line, h_artikel in db_session.query(H_bill_line, H_artikel).join(H_artikel, (H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == dept)).filter(
            (H_bill_line.departement == dept) & (H_bill_line.tischnr == tischnr) & (H_bill_line.rechnr == h_bill.rechnr)).order_by(H_bill_line._recid).all():
        if h_bill_line_obj_list.get(h_bill_line._recid):
            continue
        else:
            h_bill_line_obj_list[h_bill_line._recid] = True

        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_data.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)
        t_h_bill_line.rec_id = h_bill_line._recid

        t_h_bill_line.menu_flag = 1
        t_h_bill_line.sub_menu_betriebsnr = h_artikel.betriebsnr

        h_mjourn_obj_list = {}
        h_mjourn = H_mjourn()
        h_artikel_buff = H_artikel()
        for h_mjourn.nr, h_mjourn.anzahl, h_mjourn.request, h_mjourn._recid, h_artikel_buff.betriebsnr, h_artikel_buff._recid, h_artikel_buff.bezeich, h_artikel_buff.artnr in db_session.query(H_mjourn.nr, H_mjourn.anzahl, H_mjourn.request, H_mjourn._recid, H_artikel_buff.betriebsnr, H_artikel_buff._recid, H_artikel_buff.bezeich, H_artikel_buff.artnr).join(H_artikel_buff, (H_artikel_buff.artnr == H_mjourn.artnr) & (H_artikel_buff.departement == dept)).filter(
                (H_mjourn.nr == h_artikel.betriebsnr) & (H_mjourn.departement == dept) & (H_mjourn.rechnr == h_bill_line.rechnr)).order_by(H_mjourn._recid).all():
            if h_mjourn_obj_list.get(h_mjourn._recid):
                continue
            else:
                h_mjourn_obj_list[h_mjourn._recid] = True

            h_bill_line_recid = h_bill_line._recid

            if num_entries(h_mjourn.request, "|") > 1:
                if entry(0, h_mjourn.request, "|") == to_string(h_bill_line_recid):
                    t_h_bill_line = T_h_bill_line()
                    t_h_bill_line_data.append(t_h_bill_line)

                    t_h_bill_line.menu_flag = 2
                    t_h_bill_line.sub_menu_bezeich = h_artikel_buff.bezeich
                    t_h_bill_line.sub_menu_betriebsnr = h_mjourn.nr
                    t_h_bill_line.sub_menu_qty = h_mjourn.anzahl
                    t_h_bill_line.rec_id = h_bill_line_recid
                    t_h_bill_line.artnr = h_artikel_buff.artnr
                    t_h_bill_line.rechnr = None
                    t_h_bill_line.bill_datum = None
                    t_h_bill_line.anzahl = None
                    t_h_bill_line.epreis = to_decimal("0.0")
                    t_h_bill_line.betrag = to_decimal("0.0")
                    t_h_bill_line.steuercode = None
                    t_h_bill_line.bezeich = None
                    t_h_bill_line.fremdwbetrag = to_decimal("0.0")
                    t_h_bill_line.zeit = None
                    t_h_bill_line.waehrungsnr = None
                    t_h_bill_line.sysdate = None
                    t_h_bill_line.departement = None
                    t_h_bill_line.prtflag = None
                    t_h_bill_line.tischnr = None
                    t_h_bill_line.kellner_nr = None
                    t_h_bill_line.nettobetrag = to_decimal("0.0")
                    t_h_bill_line.paid_flag = None
                    t_h_bill_line.betriebsnr = None
                    t_h_bill_line.segmentcode = None
                    t_h_bill_line.transferred = None

    max_lapos, menu_data, Lhbline_data = get_output(
        ts_splitbill_build_lmenubl(h_bill._recid, dept))

    return generate_output()
