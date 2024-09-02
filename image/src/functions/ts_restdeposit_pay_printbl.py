from functions.additional_functions import *
import decimal
from models import Hoteldpt, Htparam, Wgrpgen, H_artikel, Bill, Bill_line

def ts_restdeposit_pay_printbl(curr_dept:int, deposit_amt:decimal, deposit_pay:decimal, ns_billno:int, gastno:int):
    str_line = ""
    str_line2 = ""
    str_line3 = ""
    dept_name = ""
    art_name:str = ""
    depopay_art:str = ""
    str_saldo:str = ""
    depoart:int = 0
    hoteldpt = htparam = wgrpgen = h_artikel = bill = bill_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_line, str_line2, str_line3, dept_name, art_name, depopay_art, str_saldo, depoart, hoteldpt, htparam, wgrpgen, h_artikel, bill, bill_line


        return {"str_line": str_line, "str_line2": str_line2, "str_line3": str_line3, "dept_name": dept_name}


    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == curr_dept)).first()

    if hoteldpt:
        dept_name = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1361)).first()

    if htparam:
        depoart = htparam.finteger

    wgrpgen = db_session.query(Wgrpgen).filter(
            (Wgrpgen.bezeich.op("~")(".*deposit.*"))).first()

    if wgrpgen:

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.endkum == wgrpgen.eknr) &  (H_artikel.activeflag)).first()

        if h_artikel:
            art_name = h_artikel.bezeich
    str_line = to_string(art_name, "x(15)") + " " + to_string(deposit_amt, "->>,>>>,>>9.99")

    bill = db_session.query(Bill).filter(
            (Bill.rechnr == ns_billno) &  (Bill.gastnr == gastno) &  (Bill.resnr == 0) &  (Bill.reslinnr == 1) &  (Billtyp == curr_dept) &  (Bill.flag == 1)).first()

    if bill:

        bill_line = db_session.query(Bill_line).filter(
                (Bill_line.rechnr == bill.rechnr) &  (Bill_line.artnr != depoart)).first()

        if bill_line:
            depopay_art = bill_line.bezeich
    str_line2 = to_string(depopay_art, "x(15)") + " " + to_string(deposit_pay, "->>,>>>,>>9.99")
    str_saldo = "Balance"
    str_line3 = to_string(str_saldo, "x(15)") + " " + to_string(0, "->>,>>>,>>9.99")

    return generate_output()