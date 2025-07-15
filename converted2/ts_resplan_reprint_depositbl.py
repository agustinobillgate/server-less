#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Bill_line, Hoteldpt, Htparam, Queasy, Bill, Wgrpgen, H_artikel

def ts_resplan_reprint_depositbl(curr_dept:int, s_recid:int):

    prepare_cache ([Bill_line, Hoteldpt, Htparam, Queasy, Bill, Wgrpgen, H_artikel])

    pax = 0
    guest_name = ""
    telefon = ""
    voucher_str = ""
    str_line = ""
    str_line2 = ""
    str_line3 = ""
    dept_name = ""
    time_rsv = ""
    depo_flag = False
    art_name:string = ""
    depopay_art:string = ""
    str_saldo:string = ""
    str1:string = ""
    depoart:int = 0
    ns_billno:int = 0
    guest_no:int = 0
    depo_amount:Decimal = to_decimal("0.0")
    depo_payment:Decimal = to_decimal("0.0")
    date_depopay:date = None
    bill_line = hoteldpt = htparam = queasy = bill = wgrpgen = h_artikel = None

    buf_bline = None

    Buf_bline = create_buffer("Buf_bline",Bill_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pax, guest_name, telefon, voucher_str, str_line, str_line2, str_line3, dept_name, time_rsv, depo_flag, art_name, depopay_art, str_saldo, str1, depoart, ns_billno, guest_no, depo_amount, depo_payment, date_depopay, bill_line, hoteldpt, htparam, queasy, bill, wgrpgen, h_artikel
        nonlocal curr_dept, s_recid
        nonlocal buf_bline


        nonlocal buf_bline

        return {"pax": pax, "guest_name": guest_name, "telefon": telefon, "voucher_str": voucher_str, "str_line": str_line, "str_line2": str_line2, "str_line3": str_line3, "dept_name": dept_name, "time_rsv": time_rsv, "depo_flag": depo_flag}


    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

    if hoteldpt:
        dept_name = hoteldpt.depart

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1361)]})

    if htparam:
        depoart = htparam.finteger

    queasy = get_cache (Queasy, {"_recid": [(eq, s_recid)]})

    if queasy:
        pax = queasy.number3
        guest_name = entry(0, queasy.char2, "&&")
        telefon = trim(substring(queasy.char1, 9))
        time_rsv = substring(queasy.char1, 0, 2) + ":" + substring(queasy.char1, 2, 2) + " - " + substring(queasy.char1, 4, 2) + ":" + substring(queasy.char1, 6, 2)
        guest_no = to_int(entry(2, queasy.char2, "&&"))
        depo_amount =  to_decimal(queasy.deci1)
        ns_billno = to_int(queasy.deci2)

        bill = get_cache (Bill, {"rechnr": [(eq, ns_billno)],"gastnr": [(eq, guest_no)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"billtyp": [(eq, curr_dept)],"flag": [(eq, 1)]})

        if bill:

            bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"artnr": [(ne, depoart)]})

            if bill_line:
                depo_payment =  to_decimal(bill_line.betrag)
                date_depopay = bill_line.bill_datum
                depopay_art = bill_line.bezeich


                depo_flag = True

            buf_bline = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"artnr": [(eq, depoart)]})

            if buf_bline:
                str1 = entry(0, bill_line.bezeich, "[")
                voucher_str = trim(entry(1, str1, "/"))

        wgrpgen = db_session.query(Wgrpgen).filter(
                 (matches(Wgrpgen.bezeich,"*deposit*"))).first()

        if wgrpgen:

            h_artikel = db_session.query(H_artikel).filter(
                     (H_artikel.endkum == wgrpgen.eknr) & (H_artikel.activeflag)).first()

            if h_artikel:
                art_name = h_artikel.bezeich
        str_line = to_string(art_name, "x(15)") + " " + to_string(depo_amount, "->>,>>>,>>9.99")
        str_line2 = to_string(depopay_art, "x(15)") + " " + to_string(depo_payment, "->>,>>>,>>9.99")
        str_saldo = "Balance"
        str_line3 = to_string(str_saldo, "x(15)") + " " + to_string(0, "->>,>>>,>>9.99")

    return generate_output()