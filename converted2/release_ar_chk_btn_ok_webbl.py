#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Debitor, Artikel, Guest, Htparam

def release_ar_chk_btn_ok_webbl(pvilanguage:int, artnr:int, bill_no:int, datum:date, saldo:Decimal, debt_counter:int):

    prepare_cache ([Debitor, Artikel, Guest, Htparam])

    msg_str = ""
    msg_str2 = ""
    rec_id_debitor = 0
    pay_list_data = []
    lvcarea:string = "release-ar"
    tot_anz:int = 0
    debitor = artikel = guest = htparam = None

    pay_list = debt = art1 = None

    pay_list_data, Pay_list = create_model("Pay_list", {"artnr":int, "paynr":int, "datum":date, "saldo":Decimal, "bezeich":string, "s_recid":int})

    Debt = create_buffer("Debt",Debitor)
    Art1 = create_buffer("Art1",Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, rec_id_debitor, pay_list_data, lvcarea, tot_anz, debitor, artikel, guest, htparam
        nonlocal pvilanguage, artnr, bill_no, datum, saldo, debt_counter
        nonlocal debt, art1


        nonlocal pay_list, debt, art1
        nonlocal pay_list_data

        return {"msg_str": msg_str, "msg_str2": msg_str2, "rec_id_debitor": rec_id_debitor, "pay-list": pay_list_data}

    debitor = get_cache (Debitor, {"artnr": [(eq, artnr)],"counter": [(eq, debt_counter)],"rechnr": [(eq, bill_no)],"rgdatum": [(eq, datum)],"saldo": [(eq, saldo)],"opart": [(eq, 2)],"zahlkonto": [(eq, 0)]})

    if not debitor:

        debt = get_cache (Debitor, {"artnr": [(eq, artnr)],"rechnr": [(eq, bill_no)],"opart": [(eq, 1)],"zahlkonto": [(gt, 0)]})

        if debt:

            debitor = get_cache (Debitor, {"artnr": [(eq, artnr)],"counter": [(eq, debt_counter)],"rechnr": [(eq, bill_no)],"rgdatum": [(eq, datum)],"saldo": [(eq, saldo)],"opart": [(eq, 0)],"zahlkonto": [(eq, 0)]})

    if not debitor:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("No such A/R record found!", lvcarea, "")

        return generate_output()
    pay_list_data.clear()

    for debt in db_session.query(Debt).filter(
             (Debt.counter == debitor.counter) & (Debt.zahlkonto > 0)).order_by(Debt.rgdatum).all():

        artikel = get_cache (Artikel, {"artnr": [(eq, debt.zahlkonto)],"departement": [(eq, 0)]})
        pay_list = Pay_list()
        pay_list_data.append(pay_list)

        pay_list.datum = debt.rgdatum
        pay_list.artnr = debt.artnr
        pay_list.paynr = artikel.artnr
        pay_list.saldo =  to_decimal(debt.saldo)
        pay_list.bezeich = artikel.bezeich
        pay_list.s_recid = debt._recid
        tot_anz = tot_anz + 1

    guest = get_cache (Guest, {"gastnr": [(eq, debitor.gastnr)]})

    if tot_anz > 1:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Double click the payment record to cancel the payment", lvcarea, "") + chr_unicode(10) + translateExtended ("Bill Receiver : ", lvcarea, "") + guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

        return generate_output()

    art1 = get_cache (Artikel, {"artnr": [(eq, pay_list.paynr)],"departement": [(eq, 0)]})

    if art1:

        if art1.artart == 2 or art1.artart == 7:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Cancel payment not possible for this type of payment article.", lvcarea, "")

            return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1014)]})

    debt = get_cache (Debitor, {"counter": [(eq, debitor.counter)],"opart": [(ge, 1)],"zahlkonto": [(ne, 0)],"rgdatum": [(le, htparam.fdate)]})

    if debt:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("A/R Payment transferred to G/L - Cancel no longer possible.", lvcarea, "")

        return generate_output()
    msg_str2 = msg_str2 + chr_unicode(2) + "&Q" + translateExtended ("Do you really want to release the A/R payment record", lvcarea, "") + chr_unicode(10) + translateExtended ("Bill Receiver : ", lvcarea, "") + guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma + "?"
    rec_id_debitor = debitor._recid

    return generate_output()