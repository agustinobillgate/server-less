#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import Debitor, Umsatz, Htparam, Billjournal, Guest, Res_history

def release_arbl(rec_id_debitor:int, saldo:Decimal, bill_no:int, artnr:int, bediener_nr:int, bediener_userinit:string):

    prepare_cache ([Umsatz, Htparam, Billjournal, Res_history])

    counter:int = 0
    pay_amount:Decimal = to_decimal("0.0")
    debt_no:int = 0
    debitor = umsatz = htparam = billjournal = guest = res_history = None

    debt = None

    Debt = create_buffer("Debt",Debitor)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal counter, pay_amount, debt_no, debitor, umsatz, htparam, billjournal, guest, res_history
        nonlocal rec_id_debitor, saldo, bill_no, artnr, bediener_nr, bediener_userinit
        nonlocal debt


        nonlocal debt

        return {}

    debitor = db_session.query(Debitor).filter(Debitor._recid == rec_id_debitor).first()

    counter = debitor.counter

    for debt in db_session.query(Debt).filter(
                 (Debt.counter == counter) & (Debt.opart >= 1) & (Debt.zahlkonto != 0)).order_by(Debt._recid).all():

        umsatz = db_session.query(Umsatz).filter(
                 (Umsatz.departement == 0) & (Umsatz.artnr == debt.zahlkonto) & (Umsatz.datum == debt.rgdatum)).with_for_update().first()
        
        pay_amount =  to_decimal(debt.saldo)
        debt_no = debt.zahlkonto

        if umsatz:
            umsatz.anzahl = umsatz.anzahl - 1
            umsatz.betrag =  to_decimal(umsatz.betrag) - to_decimal(debt.saldo)
            pass
        db_session.delete(debt)
    
    db_session.refresh(debitor, with_for_update=True)
    debitor.opart = 0
    debitor.counter = 0

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billjournal = Billjournal()
    db_session.add(billjournal)

    billjournal.rechnr = bill_no
    billjournal.bill_datum = htparam.fdate
    billjournal.artnr = artnr
    billjournal.bezeich = "Release A/R Payment " + to_string(saldo) + ";" + to_string(pay_amount) + ";" + to_string(debt_no)
    billjournal.zinr = debitor.zinr
    billjournal.anzahl = 1
    billjournal.zeit = get_current_time_in_seconds()
    billjournal.bediener_nr = bediener_nr
    billjournal.userinit = bediener_userinit

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
            " | Debt No : " + to_string(debt_no) +\
            " | Bill Receiver : "+ guest.name +\
            "," + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma + "?"


    res_history.action = "Cancel A/R Payment"

    return generate_output()