#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Hoteldpt, Htparam, Wgrpgen, H_artikel, Bill, Bill_line

def ts_restdeposit_pay_printbl(curr_dept:int, deposit_amt:Decimal, deposit_pay:Decimal, ns_billno:int, gastno:int):

    prepare_cache ([Hoteldpt, Htparam, Wgrpgen, H_artikel, Bill, Bill_line])

    str_line = ""
    str_line2 = ""
    str_line3 = ""
    dept_name = ""
    art_name:string = ""
    depopay_art:string = ""
    str_saldo:string = ""
    depoart:int = 0
    hoteldpt = htparam = wgrpgen = h_artikel = bill = bill_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_line, str_line2, str_line3, dept_name, art_name, depopay_art, str_saldo, depoart, hoteldpt, htparam, wgrpgen, h_artikel, bill, bill_line
        nonlocal curr_dept, deposit_amt, deposit_pay, ns_billno, gastno

        return {"str_line": str_line, "str_line2": str_line2, "str_line3": str_line3, "dept_name": dept_name}


    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, curr_dept)]})

    if hoteldpt:
        dept_name = hoteldpt.depart

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1361)]})

    if htparam:
        depoart = htparam.finteger

    wgrpgen = db_session.query(Wgrpgen).filter(
             (matches(Wgrpgen.bezeich,"*deposit*"))).first()

    if wgrpgen:

        h_artikel = db_session.query(H_artikel).filter(
                 (H_artikel.endkum == wgrpgen.eknr) & (H_artikel.activeflag)).first()

        if h_artikel:
            art_name = h_artikel.bezeich
    str_line = to_string(art_name, "x(15)") + " " + to_string(deposit_amt, "->>,>>>,>>9.99")

    bill = get_cache (Bill, {"rechnr": [(eq, ns_billno)],"gastnr": [(eq, gastno)],"resnr": [(eq, 0)],"reslinnr": [(eq, 1)],"billtyp": [(eq, curr_dept)],"flag": [(eq, 1)]})

    if bill:

        bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)],"artnr": [(ne, depoart)]})

        if bill_line:
            depopay_art = bill_line.bezeich
    str_line2 = to_string(depopay_art, "x(15)") + " " + to_string(deposit_pay, "->>,>>>,>>9.99")
    str_saldo = "Balance"
    str_line3 = to_string(str_saldo, "x(15)") + " " + to_string(0, "->>,>>>,>>9.99")

    return generate_output()