from functions.additional_functions import *
import decimal
from models import Bill_line, Billjournal

def foinv_split_blinebl(split_amount:decimal, user_init:str, price_decimal:int, rec_id:int):
    bill_line = billjournal = None

    bline = None

    Bline = Bill_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_line, billjournal
        nonlocal bline


        nonlocal bline
        return {}

    def split_bill_line():

        nonlocal bill_line, billjournal
        nonlocal bline


        nonlocal bline

        fact:decimal = 0
        epreis:decimal = 0
        amount:decimal = 0
        famount:decimal = 0
        Bline = Bill_line
        fact = split_amount / bill_line.betrag
        epreis = bill_line.epreis
        amount = bill_line.betrag
        famount = bill_line.fremdwbetrag


        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill_line.rechnr
        billjournal.artnr = bill_line.artnr
        billjournal.anzahl = - bill_line.anzahl
        billjournal.fremdwaehrng = - bill_line.fremdwbetrag
        billjournal.betrag = - bill_line.betrag
        billjournal.bezeich = bill_line.bezeich
        billjournal.zinr = bill_line.zinr
        billjournal.departement = bill_line.departement
        billjournal.epreis = bill_line.epreis
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_line.bill_datum

        bill_line = db_session.query(Bill_line).first()
        bill_line.sysdate = get_current_date()
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = user_init
        bill_line.epreis = round(bill_line.epreis * (1 - fact) , price_decimal)
        bill_line.betrag = bill_line.betrag - split_amount
        bill_line.fremdwbetrag = round(bill_line.fremdwbetrag * (1 - fact) , 6)

        if substring(bill_line.bezeich, len(bill_line.bezeich) - 1, 1) != "&":
            bill_line.bezeich = bill_line.bezeich + "&"

        bill_line = db_session.query(Bill_line).first()
        bline = Bline()
        db_session.add(bline)

        buffer_copy(bill_line, bline)
        bline.epreis = round(epreis * fact, price_decimal)
        bline.betrag = split_amount
        bline.fremdwbetrag = round(famount * fact, 6)

        bline = db_session.query(Bline).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill_line.rechnr
        billjournal.artnr = bill_line.artnr
        billjournal.anzahl = bill_line.anzahl
        billjournal.fremdwaehrng = bill_line.fremdwbetrag
        billjournal.betrag = bill_line.betrag
        billjournal.bezeich = bill_line.bezeich
        billjournal.zinr = bill_line.zinr
        billjournal.departement = bill_line.departement
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bill_line.bill_datum


        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bline.rechnr
        billjournal.artnr = bline.artnr
        billjournal.anzahl = bline.anzahl
        billjournal.fremdwaehrng = bline.fremdwbetrag
        billjournal.betrag = bline.betrag
        billjournal.bezeich = bline.bezeich
        billjournal.zinr = bline.zinr
        billjournal.departement = bline.departement
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = user_init
        billjournal.bill_datum = bline.bill_datum


    bill_line = db_session.query(Bill_line).filter(
            (Bill_line._recid == rec_id)).first()
    split_bill_line()

    return generate_output()