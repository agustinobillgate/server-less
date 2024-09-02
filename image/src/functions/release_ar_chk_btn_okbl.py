from functions.additional_functions import *
import decimal
from datetime import date
from models import Debitor, Artikel, Guest, Htparam

def release_ar_chk_btn_okbl(pvilanguage:int, artnr:int, bill_no:int, datum:date, saldo:decimal):
    msg_str = ""
    msg_str2 = ""
    rec_id_debitor = 0
    pay_list_list = []
    lvcarea:str = "release_ar"
    tot_anz:int = 0
    debitor = artikel = guest = htparam = None

    pay_list = debt = art1 = None

    pay_list_list, Pay_list = create_model("Pay_list", {"artnr":int, "paynr":int, "datum":date, "saldo":decimal, "bezeich":str, "s_recid":int})

    Debt = Debitor
    Art1 = Artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, rec_id_debitor, pay_list_list, lvcarea, tot_anz, debitor, artikel, guest, htparam
        nonlocal debt, art1


        nonlocal pay_list, debt, art1
        nonlocal pay_list_list
        return {"msg_str": msg_str, "msg_str2": msg_str2, "rec_id_debitor": rec_id_debitor, "pay-list": pay_list_list}

    debitor = db_session.query(Debitor).filter(
            (Debitor.artnr == artnr) &  (Debitor.rechnr == bill_no) &  (Debitor.rgdatum == datum) &  (Debitor.saldo == saldo) &  (Debitor.opart == 2) &  (Debitor.zahlkonto == 0)).first()

    if not debitor:

        debt = db_session.query(Debt).filter(
                (Debt.artnr == artnr) &  (Debt.rechnr == bill_no) &  (Debt.opart == 1) &  (Debt.zahlkonto > 0)).first()

        if debt:

            debitor = db_session.query(Debitor).filter(
                    (Debitor.artnr == artnr) &  (Debitor.rechnr == bill_no) &  (Debitor.rgdatum == datum) &  (Debitor.saldo == saldo) &  (Debitor.opart == 0) &  (Debitor.zahlkonto == 0)).first()

    if not debitor:
        msg_str = msg_str + chr(2) + translateExtended ("No such A/R record found!", lvcarea, "")

        return generate_output()
    pay_list_list.clear()

    for debt in db_session.query(Debt).filter(
            (Debt.counter == debitor.counter) &  (Debt.zahlkonto > 0)).all():

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == debt.zahlkonto) &  (Artikel.departement == 0)).first()
        pay_list = Pay_list()
        pay_list_list.append(pay_list)

        pay_list.datum = debt.rgdatum
        pay_list.artnr = debt.artnr
        pay_list.paynr = artikel.artnr
        pay_list.saldo = debt.saldo
        pay_list.bezeich = artikel.bezeich
        pay_list.s_recid = debt._recid
        tot_anz = tot_anz + 1

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == debitor.gastnr)).first()

    if tot_anz > 1:
        msg_str = msg_str + chr(2) + translateExtended ("Double click the payment record to cancel the payment", lvcarea, "") + chr(10) + translateExtended ("Bill Receiver : ", lvcarea, "") + guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

        return generate_output()

    art1 = db_session.query(Art1).filter(
            (Art1.artnr == pay_list.paynr) &  (Art1.departement == 0)).first()

    if art1.artart == 2 or art1.artart == 7:
        msg_str = msg_str + chr(2) + translateExtended ("Cancel payment not possible for this type of payment article.", lvcarea, "")

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1014)).first()

    debt = db_session.query(Debt).filter(
            (Debt.counter == debitor.counter) &  (Debt.opart >= 1) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= htparam.fdate)).first()

    if debt:
        msg_str = msg_str + chr(2) + translateExtended ("A/R Payment transferred to G/L - Cancel no longer possible.", lvcarea, "")

        return generate_output()
    msg_str2 = msg_str2 + chr(2) + "&Q" + translateExtended ("Do you really want to release the A/R payment record", lvcarea, "") + chr(10) + translateExtended ("Bill Receiver : ", lvcarea, "") + guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma + "?"
    rec_id_debitor = debitor._recid

    return generate_output()