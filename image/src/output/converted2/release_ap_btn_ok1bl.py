#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_kredit, Artikel, L_lieferant, Htparam

def release_ap_btn_ok1bl(pvilanguage:int, bill_no:string, datum:date, saldo:Decimal):

    prepare_cache ([L_kredit, Artikel, L_lieferant, Htparam])

    msg_str = ""
    msg_str2 = ""
    rec_id = 0
    pay_list_list = []
    lvcarea:string = "mk-gcPI"
    tot_anz:int = 0
    l_kredit = artikel = l_lieferant = htparam = None

    pay_list = debt = None

    pay_list_list, Pay_list = create_model("Pay_list", {"datum":date, "saldo":Decimal, "bezeich":string, "s_recid":int})

    Debt = create_buffer("Debt",L_kredit)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, rec_id, pay_list_list, lvcarea, tot_anz, l_kredit, artikel, l_lieferant, htparam
        nonlocal pvilanguage, bill_no, datum, saldo
        nonlocal debt


        nonlocal pay_list, debt
        nonlocal pay_list_list

        return {"msg_str": msg_str, "msg_str2": msg_str2, "rec_id": rec_id, "pay-list": pay_list_list}

    l_kredit = get_cache (L_kredit, {"lscheinnr": [(eq, bill_no)],"rgdatum": [(eq, datum)],"saldo": [(eq, saldo)],"zahlkonto": [(eq, 0)],"counter": [(ne, 0)]})

    if not l_kredit:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("No such A/P record found!", lvcarea, "")

        return generate_output()

    if l_kredit.counter == 0:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("This A/P has no payment record!", lvcarea, "")

        return generate_output()
    pay_list_list.clear()

    for debt in db_session.query(Debt).filter(
             (Debt.counter == l_kredit.counter) & (Debt.zahlkonto > 0)).order_by(Debt.rgdatum).all():

        artikel = get_cache (Artikel, {"artnr": [(eq, debt.zahlkonto)]})
        pay_list = Pay_list()
        pay_list_list.append(pay_list)

        pay_list.datum = debt.rgdatum
        pay_list.saldo =  to_decimal(debt.saldo)
        pay_list.bezeich = artikel.bezeich
        pay_list.s_recid = debt._recid
        tot_anz = tot_anz + 1

    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_kredit.lief_nr)]})

    if tot_anz > 1:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Double click the payment record to cancel the payment.", lvcarea, "") + chr_unicode(10) + translateExtended ("Supplier Name :", lvcarea, "") + " " + l_lieferant.firma

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1118)]})

    debt = get_cache (L_kredit, {"counter": [(eq, l_kredit.counter)],"opart": [(ge, 1)],"zahlkonto": [(ne, 0)],"rgdatum": [(le, htparam.fdate)]})

    if debt:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("A/P Payment transferred to G/L - Cancel no longer possible.", lvcarea, "")

        return generate_output()
    msg_str2 = msg_str2 + chr_unicode(2) + "&Q" + translateExtended ("Do you really want to release ALL A/P payment record(s).", lvcarea, "") + chr_unicode(10) + translateExtended ("Supplier Name :", lvcarea, "") + " " + l_lieferant.firma + "?"
    rec_id = l_kredit._recid

    return generate_output()