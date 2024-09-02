from functions.additional_functions import *
import decimal
from datetime import date
from models import Bill_line, Hoteldpt, Htparam, Queasy, Bill, Wgrpgen, H_artikel

def ts_resplan_reprint_depositbl(curr_dept:int, s_recid:int):
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
    art_name:str = ""
    depopay_art:str = ""
    str_saldo:str = ""
    str1:str = ""
    depoart:int = 0
    ns_billno:int = 0
    guest_no:int = 0
    depo_amount:decimal = 0
    depo_payment:decimal = 0
    date_depopay:date = None
    bill_line = hoteldpt = htparam = queasy = bill = wgrpgen = h_artikel = None

    buf_bline = None

    Buf_bline = Bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pax, guest_name, telefon, voucher_str, str_line, str_line2, str_line3, dept_name, time_rsv, depo_flag, art_name, depopay_art, str_saldo, str1, depoart, ns_billno, guest_no, depo_amount, depo_payment, date_depopay, bill_line, hoteldpt, htparam, queasy, bill, wgrpgen, h_artikel
        nonlocal buf_bline


        nonlocal buf_bline
        return {"pax": pax, "guest_name": guest_name, "telefon": telefon, "voucher_str": voucher_str, "str_line": str_line, "str_line2": str_line2, "str_line3": str_line3, "dept_name": dept_name, "time_rsv": time_rsv, "depo_flag": depo_flag}


    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == curr_dept)).first()

    if hoteldpt:
        dept_name = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1361)).first()

    if htparam:
        depoart = htparam.finteger

    queasy = db_session.query(Queasy).filter(
            (Queasy._recid == s_recid)).first()

    if queasy:
        pax = queasy.number3
        guest_name = entry(0, queasy.char2, "&&")
        telefon = trim(substring(queasy.char1, 9))
        time_rsv = substring(queasy.char1, 0, 2) + ":" + substring(queasy.char1, 2, 2) + " - " + substring(queasy.char1, 4, 2) + ":" + substring(queasy.char1, 6, 2)
        guest_no = to_int(entry(2, queasy.char2, "&&"))
        depo_amount = queasy.deci1
        ns_billno = to_int(queasy.deci2)

        bill = db_session.query(Bill).filter(
                (Bill.rechnr == ns_billno) &  (Bill.gastnr == guest_no) &  (Bill.resnr == 0) &  (Bill.reslinnr == 1) &  (Billtyp == curr_dept) &  (Bill.flag == 1)).first()

        if bill:

            bill_line = db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == bill.rechnr) &  (Bill_line.artnr != depoart)).first()

            if bill_line:
                depo_payment = bill_line.betrag
                date_depopay = bill_line.bill_datum
                depopay_art = bill_line.bezeich


                depo_flag = True

            buf_bline = db_session.query(Buf_bline).filter(
                    (Buf_bline.rechnr == bill.rechnr) &  (Buf_bline.artnr == depoart)).first()

            if buf_bline:
                str1 = entry(0, bill_line.bezeich, "[")
                voucher_str = trim(entry(1, str1, "/"))

        wgrpgen = db_session.query(Wgrpgen).filter(
                (Wgrpgen.bezeich.op("~")(".*deposit.*"))).first()

        if wgrpgen:

            h_artikel = db_session.query(H_artikel).filter(
                    (H_artikel.endkum == wgrpgen.eknr) &  (H_artikel.activeflag)).first()

            if h_artikel:
                art_name = h_artikel.bezeich
        str_line = to_string(art_name, "x(15)") + " " + to_string(depo_amount, "->>,>>>,>>9.99")
        str_line2 = to_string(depopay_art, "x(15)") + " " + to_string(depo_payment, "->>,>>>,>>9.99")
        str_saldo = "Balance"
        str_line3 = to_string(str_saldo, "x(15)") + " " + to_string(0, "->>,>>>,>>9.99")

    return generate_output()