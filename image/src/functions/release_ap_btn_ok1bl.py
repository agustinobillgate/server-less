from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_kredit, Artikel, L_lieferant, Htparam

def release_ap_btn_ok1bl(pvilanguage:int, bill_no:str, datum:date, saldo:decimal):
    msg_str = ""
    msg_str2 = ""
    rec_id = 0
    pay_list_list = []
    lvcarea:str = "mk_gcPI"
    tot_anz:int = 0
    l_kredit = artikel = l_lieferant = htparam = None

    pay_list = debt = None

    pay_list_list, Pay_list = create_model("Pay_list", {"datum":date, "saldo":decimal, "bezeich":str, "s_recid":int})

    Debt = L_kredit

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, rec_id, pay_list_list, lvcarea, tot_anz, l_kredit, artikel, l_lieferant, htparam
        nonlocal debt


        nonlocal pay_list, debt
        nonlocal pay_list_list
        return {"msg_str": msg_str, "msg_str2": msg_str2, "rec_id": rec_id, "pay-list": pay_list_list}

    l_kredit = db_session.query(L_kredit).filter(
            (func.lower(L_kredit.lscheinnr) == (bill_no).lower()) &  (L_kredit.rgdatum == datum) &  (L_kredit.saldo == saldo) &  (L_kredit.zahlkonto == 0) &  (L_kredit.counter != 0)).first()

    if not l_kredit:
        msg_str = msg_str + chr(2) + translateExtended ("No such A/P record found!", lvcarea, "")

        return generate_output()

    if l_kredit.counter == 0:
        msg_str = msg_str + chr(2) + translateExtended ("This A/P has no payment record!", lvcarea, "")

        return generate_output()
    pay_list_list.clear()

    for debt in db_session.query(Debt).filter(
            (Debt.counter == l_kredit.counter) &  (Debt.zahlkonto > 0)).all():

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == debt.zahlkonto)).first()
        pay_list = Pay_list()
        pay_list_list.append(pay_list)

        pay_list.datum = debt.rgdatum
        pay_list.saldo = debt.saldo
        pay_list.bezeich = artikel.bezeich
        pay_list.s_recid = debt._recid
        tot_anz = tot_anz + 1
    OPEN QUERY q1 FOR EACH pay_list

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant.lief_nr == l_kredit.lief_nr)).first()

    if tot_anz > 1:
        msg_str = msg_str + chr(2) + translateExtended ("Double click the payment record to cancel the payment.", lvcarea, "") + chr(10) + translateExtended ("Supplier Name :", lvcarea, "") + " " + l_lieferant.firma

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1118)).first()

    debt = db_session.query(Debt).filter(
            (Debt.counter == l_kredit.counter) &  (Debt.opart >= 1) &  (Debt.zahlkonto != 0) &  (Debt.rgdatum <= htparam.fdate)).first()

    if debt:
        msg_str = msg_str + chr(2) + translateExtended ("A/P Payment transferred to G/L - Cancel no longer possible.", lvcarea, "")

        return generate_output()
    msg_str2 = msg_str2 + chr(2) + "&Q" + translateExtended ("Do you really want to release ALL A/P payment record(s).", lvcarea, "") + chr(10) + translateExtended ("Supplier Name :", lvcarea, "") + " " + l_lieferant.firma + "?"
    rec_id = l_kredit._recid

    return generate_output()