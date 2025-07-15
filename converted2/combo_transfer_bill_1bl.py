from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Bill, Htparam, Artikel, Counters, Umsatz, Bill_line, Billjournal, Res_line

def combo_transfer_bill_1bl(pvilanguage:int, dept_type:int, dept:int, dept_bezeich:str, h_bill_rechnr:int, transdate:date, double_currency:bool, exchg_rate:decimal, bilrecid:int, foreign_rate:bool, user_init:str, amount:decimal, amount_foreign:decimal):
    bill_descript = ""
    success_flag = False
    msg_str = ""
    gname = ""
    bill_date:date = None
    billart:int = 0
    qty:int = 0
    descript_str:str = ""
    error_flag:bool = False
    lvcarea:str = "ts-restinv"
    dept_char:str = " >>*"
    bill = htparam = artikel = counters = umsatz = bill_line = billjournal = res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_descript, success_flag, msg_str, gname, bill_date, billart, qty, descript_str, error_flag, lvcarea, dept_char, bill, htparam, artikel, counters, umsatz, bill_line, billjournal, res_line
        nonlocal pvilanguage, dept_type, dept, dept_bezeich, h_bill_rechnr, transdate, double_currency, exchg_rate, bilrecid, foreign_rate, user_init, amount, amount_foreign


        return {"bill_descript": bill_descript, "success_flag": success_flag, "msg_str": msg_str, "gname": gname}


    if dept_type == 0:
        dept_char = " ^^*"

    if amount == 0:

        return generate_output()

    bill = db_session.query(Bill).filter(
             (Bill._recid == bilrecid)).first()

    if transdate != None:
        bill_date = transdate
    else:
        bill_date = get_output(htpdate(110))

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 253)).first()

        if htparam.flogical and bill_date < get_current_date():
            bill_date = bill_date + timedelta(days=1)
    billart = 0
    qty = 1

    if not double_currency:
        amount_foreign =  to_decimal(amount) / to_decimal(exchg_rate)

    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 245)).first()

    artikel = db_session.query(Artikel).filter(
                 (Artikel.artnr == htparam.finteger) & (Artikel.departement == 0)).first()

    if not artikel:
        msg_str = translateExtended ("Combo FO Artno not defined. (Param 245 / Grp 7)", lvcarea, "") +\
                chr(10)
        error_flag = True

    elif artikel.artart != 0:
        msg_str = translateExtended ("Combo FO Artno has wrong Article Type. (Param 245)", lvcarea, "") +\
                chr(10)
        error_flag = True

    if error_flag:

        return generate_output()

    if bill.rechnr == 0:

        counters = db_session.query(Counters).filter(
                     (Counters.counter_no == 3)).first()
        counters.counter = counters.counter + 1
        bill.rechnr = counters.counter

    if bill.datum < bill_date:
        bill.datum = bill_date
    bill.saldo =  to_decimal(bill.saldo) + to_decimal(amount)
    bill.mwst[98] = bill.mwst[98] + amount_foreign
    bill.rgdruck = 0

    if artikel:
        billart = artikel.artnr
        descript_str = dept_bezeich + dept_char +\
            to_string(h_bill_rechnr)


    else:
        descript_str = dept_bezeich + dept_char + to_string(h_bill_rechnr)

    umsatz = db_session.query(Umsatz).filter(
                     (Umsatz.artnr == billart) & (Umsatz.departement == 0) & (Umsatz.datum == bill_date)).first()

    if not umsatz:
        umsatz = Umsatz()
        db_session.add(umsatz)

        umsatz.artnr = billart
        umsatz.datum = bill_date
        umsatz.departement = 0


    umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(amount)
    umsatz.anzahl = umsatz.anzahl + 1


    bill_line = Bill_line()
    db_session.add(bill_line)

    bill_line.rechnr = bill.rechnr
    bill_line.zinr = bill.zinr
    bill_line.massnr = bill.resnr
    bill_line.billin_nr = bill.reslinnr
    bill_line.artnr = billart
    bill_line.bezeich = descript_str
    bill_line.anzahl = 1
    bill_line.fremdwbetrag =  to_decimal(amount_foreign)
    bill_line.betrag =  to_decimal(amount)
    bill_line.departement = 0
    bill_line.epreis =  to_decimal("0")
    bill_line.zeit = get_current_time_in_seconds()
    bill_line.userinit = user_init
    bill_line.bill_datum = bill_date


    billjournal = Billjournal()
    db_session.add(billjournal)

    billjournal.rechnr = bill.rechnr
    billjournal.zinr = bill.zinr
    billjournal.departement = 0
    billjournal.artnr = billart
    billjournal.anzahl = 1
    billjournal.fremdwaehrng =  to_decimal(amount_foreign)
    billjournal.betrag =  to_decimal(amount)
    billjournal.bezeich = descript_str
    billjournal.epreis =  to_decimal("0")
    billjournal.zeit = get_current_time_in_seconds()
    billjournal.stornogrund = ""
    billjournal.userinit = user_init
    billjournal.bill_datum = bill_date


    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == bill.resnr) & (Res_line.reslinnr == bill.parent_nr)).first()

    if res_line:
        gname = res_line.name


    bill_descript = " >>*" + to_string(bill.rechnr)
    success_flag = True

    return generate_output()