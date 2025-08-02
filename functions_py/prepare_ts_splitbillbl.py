#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 31/7/2025
# gitlab: 510
# generate_output: diff key, edit manual di generate_output
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from functions.ts_splitbill_build_lmenubl import ts_splitbill_build_lmenubl
from models import H_bill, H_bill_line, Htparam, Waehrung, Hoteldpt

def prepare_ts_splitbillbl(dept:int, tischnr:int):

    prepare_cache ([Htparam, Waehrung, Hoteldpt])

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
    h_bill = h_bill_line = htparam = waehrung = hoteldpt = None

    menu = lhbline = t_h_bill = t_h_bill_line = None

    menu_data, Menu = create_model("Menu", {"pos":int, "bezeich":string, "artnr":int})
    lhbline_data, Lhbline = create_model("Lhbline", {"nr":int, "rid":int})
    t_h_bill_data, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_h_bill_line_data, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal multi_vat, zero_flag, multi_cash, price_decimal, foreign_rate, double_currency, exchg_rate, deptname, must_print, fl_warn, max_lapos, cashless_flag, t_h_bill_data, t_h_bill_line_data, menu_data, lhbline_data, h_bill, h_bill_line, htparam, waehrung, hoteldpt
        nonlocal dept, tischnr


        nonlocal menu, lhbline, t_h_bill, t_h_bill_line
        nonlocal menu_data, lhbline_data, t_h_bill_data, t_h_bill_line_data

        # Rd 31/7/2025
        # return {"multi_vat": multi_vat, "zero_flag": zero_flag, "multi_cash": multi_cash, "price_decimal": price_decimal, "foreign_rate": foreign_rate, "double_currency": double_currency, "exchg_rate": exchg_rate, "deptname": deptname, "must_print": must_print, "fl_warn": fl_warn, "max_lapos": max_lapos, "cashless_flag": cashless_flag, "t-h-bill": t_h_bill_data, "t-h-bill-line": t_h_bill_line_data, "menu": menu_data, "Lhbline": lhbline_data}
        return {"multi_vat": multi_vat, "zero_flag": zero_flag, "multi_cash": multi_cash, "price_decimal": price_decimal, "foreign_rate": foreign_rate, "double_currency": double_currency, "exchg_rate": exchg_rate, "deptname": deptname, "mustPrint": must_print, "flWarn": fl_warn, "maxLapos": max_lapos, "cashlessFlag": cashless_flag, "t-h-bill": t_h_bill_data, "t-h-bill-line": t_h_bill_line_data, "MENU": menu_data, "Lhbline": lhbline_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 834)]})
    cashless_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 271)]})

    if htparam.feldtyp == 4:
        multi_vat = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 869)]})
    zero_flag = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 833)]})
    multi_cash = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    if foreign_rate:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})
    deptname = hoteldpt.depart

    htparam = get_cache (Htparam, {"paramnr": [(eq, 877)]})
    must_print = htparam.flogical

    h_bill = get_cache (H_bill, {"departement": [(eq, dept)],"tischnr": [(eq, tischnr)],"flag": [(eq, 0)]})

    if not h_bill:

        return generate_output()
    t_h_bill = T_h_bill()
    t_h_bill_data.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    htparam = get_cache (Htparam, {"paramnr": [(eq, 948)]})

    if htparam.paramgruppe == 19 and htparam.flogical:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 557)]})

        h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)],"departement": [(eq, dept)],"artnr": [(eq, htparam.finteger)],"betrag": [(ne, 0)]})

        if h_bill_line:
            fl_warn = True

    for h_bill_line in db_session.query(H_bill_line).filter(
             (H_bill_line.departement == dept) & (H_bill_line.tischnr == tischnr) & (H_bill_line.rechnr == h_bill.rechnr)).order_by(H_bill_line._recid).all():
        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_data.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)
        t_h_bill_line.rec_id = h_bill_line._recid


    max_lapos, menu_data, Lhbline_data = get_output(ts_splitbill_build_lmenubl(h_bill._recid, dept))

    return generate_output()