#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd 28/7/2025
# gitlab: 280
# tested di UI Baru
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Debitor, Artikel, Htparam, Umsatz, Billjournal, Guest, Res_history

def release_ar_def_actionbl(pvilanguage:int, pay_list_paynr:int, pay_list_s_recid:int, bediener_nr:int, bediener_userinit:string, artnr:int, bill_no:int, datum:date, saldo:Decimal):

    prepare_cache ([Debitor, Artikel, Htparam, Umsatz, Billjournal, Res_history])

    msg_str = ""
    lvcarea:string = "release-ar"
    i_counter:int = 0
    pay_amount:Decimal = to_decimal("0.0")
    debt_no:int = 0
    debitor = artikel = htparam = umsatz = billjournal = guest = res_history = None

    debt = bdebt = art1 = None

    Debt = create_buffer("Debt",Debitor)
    Bdebt = create_buffer("Bdebt",Debitor)
    Art1 = create_buffer("Art1",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, i_counter, pay_amount, debt_no, debitor, artikel, htparam, umsatz, billjournal, guest, res_history
        nonlocal pvilanguage, pay_list_paynr, pay_list_s_recid, bediener_nr, bediener_userinit, artnr, bill_no, datum, saldo
        nonlocal debt, bdebt, art1


        nonlocal debt, bdebt, art1

        return {"msg_str": msg_str}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 1014)]})

    debt = get_cache (Debitor, {"_recid": [(eq, pay_list_s_recid)]})

    if debt and debt.rgdatum <= htparam.fdate:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("A/R Payment transferred to G/L - Cancel no longer possible.", lvcarea, "")

        return generate_output()

    art1 = get_cache (Artikel, {"artnr": [(eq, pay_list_paynr)],"departement": [(eq, 0)]})

    if art1.artart == 2 or art1.artart == 7:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Cancel payment not possible for this type of payment article.", lvcarea, "")

        return generate_output()

    debt = get_cache (Debitor, {"_recid": [(eq, pay_list_s_recid)]})

    if debt:

        debitor = get_cache (Debitor, {"artnr": [(eq, debt.artnr)],"counter": [(eq, debt.counter)],"zahlkonto": [(eq, 0)]})

        if debitor:
            i_counter = debitor.counter
            pay_amount =  to_decimal(debt.saldo)
            debt_no = debt.zahlkonto


            pass

            umsatz = get_cache (Umsatz, {"departement": [(eq, 0)],"artnr": [(eq, debt.zahlkonto)],"datum": [(eq, debt.rgdatum)]})

            if umsatz:
                umsatz.anzahl = umsatz.anzahl - 1
                umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(debt.saldo)


                pass
            db_session.delete(debt)

            if debitor:
                pass
                debitor.opart = 0
                pass

            htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
            billjournal = Billjournal()
            db_session.add(billjournal)

            billjournal.rechnr = bill_no
            billjournal.bill_datum = htparam.fdate
            billjournal.artnr = artnr
            billjournal.bezeich = translateExtended ("Release A/R Payment", lvcarea, "") + " " + to_string(saldo) + ";" + to_string(pay_amount) + ";" + to_string(debt_no)
            billjournal.zinr = debitor.zinr
            billjournal.anzahl = 1
            billjournal.zeit = get_current_time_in_seconds()
            billjournal.bediener_nr = bediener_nr
            billjournal.userinit = bediener_userinit

            for bdebt in db_session.query(Bdebt).filter(
                     (Bdebt.counter == i_counter) & (Bdebt.zahlkonto > 0) & (Bdebt.opart == 2)).order_by(Bdebt._recid).all():
                bdebt.opart = 1

            guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener_nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Cancel A/R Payment With Bill No: " + to_string(bill_no) +\
                    " | Art No: " + to_string(artnr) +\
                    " | Balance: " + to_string(saldo) +\
                    " | Pay Amount: " + to_string(pay_amount) +\
                    " | Deb N0 : " + to_string(debt_no) +\
                    " | Bill Receiver : "+ guest.name +\
                    "," + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma + "?"


            res_history.action = "Cancel A/R Payment"

    return generate_output()