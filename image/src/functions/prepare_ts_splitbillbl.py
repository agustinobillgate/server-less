from functions.additional_functions import *
import decimal
from functions.ts_splitbill_build_lmenubl import ts_splitbill_build_lmenubl
from models import H_bill, H_bill_line, Htparam, Waehrung, Hoteldpt

def prepare_ts_splitbillbl(dept:int, tischnr:int):
    multi_vat = False
    zero_flag = False
    multi_cash = False
    price_decimal = 0
    foreign_rate = False
    double_currency = False
    exchg_rate = 0
    deptname = ""
    must_print = False
    fl_warn = False
    max_lapos = 0
    cashless_flag = False
    t_h_bill_list = []
    t_h_bill_line_list = []
    menu_list = []
    lhbline_list = []
    h_bill = h_bill_line = htparam = waehrung = hoteldpt = None

    menu = lhbline = t_h_bill = t_h_bill_line = None

    menu_list, Menu = create_model("Menu", {"pos":int, "bezeich":str, "artnr":int})
    lhbline_list, Lhbline = create_model("Lhbline", {"nr":int, "rid":int})
    t_h_bill_list, T_h_bill = create_model_like(H_bill, {"rec_id":int})
    t_h_bill_line_list, T_h_bill_line = create_model_like(H_bill_line, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal multi_vat, zero_flag, multi_cash, price_decimal, foreign_rate, double_currency, exchg_rate, deptname, must_print, fl_warn, max_lapos, cashless_flag, t_h_bill_list, t_h_bill_line_list, menu_list, lhbline_list, h_bill, h_bill_line, htparam, waehrung, hoteldpt


        nonlocal menu, lhbline, t_h_bill, t_h_bill_line
        nonlocal menu_list, lhbline_list, t_h_bill_list, t_h_bill_line_list
        return {"multi_vat": multi_vat, "zero_flag": zero_flag, "multi_cash": multi_cash, "price_decimal": price_decimal, "foreign_rate": foreign_rate, "double_currency": double_currency, "exchg_rate": exchg_rate, "deptname": deptname, "must_print": must_print, "fl_warn": fl_warn, "max_lapos": max_lapos, "cashless_flag": cashless_flag, "t-h-bill": t_h_bill_list, "t-h-bill-line": t_h_bill_line_list, "MENU": menu_list, "Lhbline": lhbline_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 834)).first()
    cashless_flag = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 271)).first()

    if htparam.feldtyp == 4:
        multi_vat = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 869)).first()
    zero_flag = flogical

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 833)).first()
    multi_cash = flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    if foreign_rate:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == dept)).first()
    deptname = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (htpara.paramnr == 877)).first()
    must_print = flogical

    h_bill = db_session.query(H_bill).filter(
            (H_bill.departement == dept) &  (H_bill.tischnr == tischnr) &  (H_bill.flag == 0)).first()
    t_h_bill = T_h_bill()
    t_h_bill_list.append(t_h_bill)

    buffer_copy(h_bill, t_h_bill)
    t_h_bill.rec_id = h_bill._recid

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 948)).first()

    if htparam.paramgruppe == 19 and htparam.flogical:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 557)).first()

        h_bill_line = db_session.query(H_bill_line).filter(
                (H_bill_line.rechnr == h_bill.rechnr) &  (H_bill_line.departement == dept) &  (H_bill_line.artnr == htparam.finteger) &  (H_bill_line.betrag != 0)).first()

        if h_bill_line:
            fl_warn = True

    for h_bill_line in db_session.query(H_bill_line).filter(
            (H_bill_line.departement == dept) &  (H_bill_line.tischnr == tischnr) &  (H_bill_line.rechnr == h_bill.rechnr)).all():
        t_h_bill_line = T_h_bill_line()
        t_h_bill_line_list.append(t_h_bill_line)

        buffer_copy(h_bill_line, t_h_bill_line)
        t_h_bill_line.rec_id = h_bill_line._recid


    max_lapos, menu_list, Lhbline_list = get_output(ts_splitbill_build_lmenubl(h_bill._recid, dept))

    return generate_output()