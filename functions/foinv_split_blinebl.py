#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bill_line, Billjournal

def foinv_split_blinebl(split_amount:Decimal, user_init:string, price_decimal:int, rec_id:int):

    prepare_cache ([Bill_line, Billjournal])

    bill_line = billjournal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_line, billjournal
        nonlocal split_amount, user_init, price_decimal, rec_id

        return {}

    def split_bill_line():

        nonlocal bill_line, billjournal
        nonlocal split_amount, user_init, price_decimal, rec_id

        fact:Decimal = to_decimal("0.0")
        epreis:Decimal = to_decimal("0.0")
        amount:Decimal = to_decimal("0.0")
        famount:Decimal = to_decimal("0.0")
        bline = None
        Bline =  create_buffer("Bline",Bill_line)

        bill_line = get_cache (Bill_line, {"_recid": [(eq, rec_id)]})

        if bill_line:
            fact =  to_decimal(split_amount) / to_decimal(bill_line.betrag)
            epreis =  to_decimal(bill_line.epreis)
            amount =  to_decimal(bill_line.betrag)
            famount =  to_decimal(bill_line.fremdwbetrag)


            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = bill_line.rechnr
            billjournal.artnr = bill_line.artnr
            billjournal.anzahl = - bill_line.anzahl
            billjournal.fremdwaehrng =  - to_decimal(bill_line.fremdwbetrag)
            billjournal.betrag =  - to_decimal(bill_line.betrag)
            billjournal.bezeich = bill_line.bezeich
            billjournal.zinr = bill_line.zinr
            billjournal.departement = bill_line.departement
            billjournal.epreis =  to_decimal(bill_line.epreis)
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.userinit = user_init
            billjournal.bill_datum = bill_line.bill_datum


            pass
            bill_line.sysdate = get_current_date()
            bill_line.zeit = get_current_time_in_seconds()
            bill_line.userinit = user_init
            bill_line.epreis = to_decimal(round(bill_line.epreis * (1 - fact) , price_decimal))
            bill_line.betrag =  to_decimal(bill_line.betrag) - to_decimal(split_amount)
            bill_line.fremdwbetrag = to_decimal(round(bill_line.fremdwbetrag * (1 - fact) , 6))

            if substring(bill_line.bezeich, length(bill_line.bezeich) - 1, 1) != ("&").lower() :
                bill_line.bezeich = bill_line.bezeich + "&"
            pass
            bline = Bill_line()
            db_session.add(bline)

            buffer_copy(bill_line, bline)
            bline.epreis = to_decimal(round(epreis * fact , price_decimal))
            bline.betrag =  to_decimal(split_amount)
            bline.fremdwbetrag = to_decimal(round(famount * fact , 6))


            pass
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = bill_line.rechnr
            billjournal.artnr = bill_line.artnr
            billjournal.anzahl = bill_line.anzahl
            billjournal.fremdwaehrng =  to_decimal(bill_line.fremdwbetrag)
            billjournal.betrag =  to_decimal(bill_line.betrag)
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
            billjournal.fremdwaehrng =  to_decimal(bline.fremdwbetrag)
            billjournal.betrag =  to_decimal(bline.betrag)
            billjournal.bezeich = bline.bezeich
            billjournal.zinr = bline.zinr
            billjournal.departement = bline.departement
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.userinit = user_init
            billjournal.bill_datum = bline.bill_datum


    split_bill_line()

    return generate_output()