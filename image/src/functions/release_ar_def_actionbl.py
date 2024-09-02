from functions.additional_functions import *
import decimal
from datetime import date
from models import Debitor, Artikel, Htparam, Umsatz, Billjournal, Guest, Res_history

def release_ar_def_actionbl(pvilanguage:int, pay_list_paynr:int, pay_list_s_recid:int, bediener_nr:int, bediener_userinit:str, artnr:int, bill_no:int, datum:date, saldo:decimal):
    msg_str = ""
    lvcarea:str = "release_ar"
    i_counter:int = 0
    pay_amount:decimal = 0
    debt_no:int = 0
    debitor = artikel = htparam = umsatz = billjournal = guest = res_history = None

    debt = art1 = None

    Debt = Debitor
    Art1 = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, i_counter, pay_amount, debt_no, debitor, artikel, htparam, umsatz, billjournal, guest, res_history
        nonlocal debt, art1


        nonlocal debt, art1
        return {"msg_str": msg_str}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1014)).first()

    debt = db_session.query(Debt).filter(
            (Debt._recid == pay_list_s_recid)).first()

    if debt and debt.rgdatum <= htparam.fdate:
        msg_str = msg_str + chr(2) + translateExtended ("A/R Payment transferred to G/L - Cancel no longer possible.", lvcarea, "")

        return generate_output()

    art1 = db_session.query(Art1).filter(
            (Art1.artnr == pay_list_paynr) &  (Art1.departement == 0)).first()

    if art1.artart == 2 or art1.artart == 7:
        msg_str = msg_str + chr(2) + translateExtended ("Cancel payment not possible for this type of payment article.", lvcarea, "")

        return generate_output()

    debitor = db_session.query(Debitor).filter(
            (Debitor.artnr == debt.artnr) &  (Debitor.counter == debt.counter) &  (Debitor.zahlkonto == 0)).first()

    if debitor:
        i_counter = debitor.counter


        pay_amount = debt.saldo
        debt_no = debt.zahlkonto

        debt = db_session.query(Debt).first()

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.departement == 0) &  (Umsatz.artnr == debt.zahlkonto) &  (Umsatz.datum == debt.rgdatum)).first()

        if umsatz:
            umsatz.anzahl = umsatz.anzahl - 1
            umsatz.betrag = umsatz.betrag - debt.saldo

    db_session.delete(debt)

    if debitor:

        debitor = db_session.query(Debitor).first()
        debitor.opart = 0

        debitor = db_session.query(Debitor).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billjournal = Billjournal()
    db_session.add(billjournal)

    billjournal.rechnr = bill_no
    billjournal.bill_datum = fdate
    billjournal.artnr = artnr
    billjournal.bezeich = translateExtended ("Release A/R Payment", lvcarea, "") + " " + to_string(saldo) + ";" + to_string(pay_amount) + ";" + to_string(debt_no)
    billjournal.zinr = debitor.zinr
    billjournal.anzahl = 1
    billjournal.zeit = get_current_time_in_seconds()
    billjournal.bediener_nr = bediener_nr
    billjournal.userinit = bediener_userinit

    for debt in db_session.query(Debt).filter(
            (Debt.counter == i_counter) &  (Debt.zahlkonto > 0) &  (Debt.opart == 2)).all():
        debt.opart = 1

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == debitor.gastnr)).first()
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