#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel, Htparam, Guest, Res_line, Bill_line, Debitor

def check_gcfpayment1_webbl(pvilanguage:int, gastnr:int, rechnr:int, resnr:int, reslinnr:int, payment:int):

    prepare_cache ([Artikel, Htparam, Guest, Res_line, Bill_line, Debitor])

    msg_str = ""
    msg_str2 = ""
    htparam_fchar = ""
    htparam_fchar1 = ""
    guest_kreditlimit = to_decimal("0.0")
    enter_passwd1 = False
    enter_passwd2 = False
    voucher_number = ""
    lvcarea:string = "check-gcfpayment"
    zahlungsart:int = 0
    outstand:Decimal = to_decimal("0.0")
    i:int = 0
    str:string = ""
    artikel = htparam = guest = res_line = bill_line = debitor = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, htparam_fchar, htparam_fchar1, guest_kreditlimit, enter_passwd1, enter_passwd2, voucher_number, lvcarea, zahlungsart, outstand, i, str, artikel, htparam, guest, res_line, bill_line, debitor
        nonlocal pvilanguage, gastnr, rechnr, resnr, reslinnr, payment

        return {"payment": payment, "msg_str": msg_str, "msg_str2": msg_str2, "htparam_fchar": htparam_fchar, "htparam_fchar1": htparam_fchar1, "guest_kreditlimit": guest_kreditlimit, "enter_passwd1": enter_passwd1, "enter_passwd2": enter_passwd2, "voucher_number": voucher_number}


    artikel = get_cache (Artikel, {"artnr": [(eq, payment)],"departement": [(eq, 0)]})

    if artikel and artikel.artart == 2:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 116)]})

        if artikel.zwkum == htparam.finteger:

            return generate_output()

        guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

        if guest:
            zahlungsart = guest.zahlungsart

        if zahlungsart == 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})

            if htparam.fchar != "":
                enter_passwd1 = True
                htparam_fchar = htparam.fchar
            else:
                msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("No C/L payment Articles have been defined for this Guest.", lvcarea, "")

        elif guest.zahlungsart != payment:

            artikel = get_cache (Artikel, {"departement": [(eq, 0)],"artnr": [(eq, guest.zahlungsart)]})

            if artikel:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("C/L payment Article for this guest is", lvcarea, "") + chr_unicode(10) + to_string(artikel.artnr) + " - " + artikel.bezeich
                payment = 0

                return generate_output()

        if guest.karteityp == 2:

            res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

            if res_line:
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 7) == ("voucher").lower() :
                        voucher_number = substring(str, 7)
                        i = 9999

        if guest.karteityp >= 1 and guest.kreditlimit > 0:

            for bill_line in db_session.query(Bill_line).filter(
                     (Bill_line.rechnr == rechnr)).order_by(Bill_line._recid).all():
                outstand =  to_decimal(outstand) + to_decimal(bill_line.betrag)

            debitor_obj_list = {}
            debitor = Debitor()
            artikel = Artikel()
            for debitor.saldo, debitor._recid, artikel.artnr, artikel.bezeich, artikel.artart, artikel.zwkum, artikel._recid in db_session.query(Debitor.saldo, Debitor._recid, Artikel.artnr, Artikel.bezeich, Artikel.artart, Artikel.zwkum, Artikel._recid).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).filter(
                     (Debitor.gastnr == guest.gastnr) & (Debitor.opart <= 1)).order_by(Debitor._recid).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True


                outstand =  to_decimal(outstand) + to_decimal(debitor.saldo)

            if outstand > guest.kreditlimit:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 320)]})

                if htparam.flogical:
                    msg_str2 = msg_str2 + chr_unicode(2) + translateExtended ("Over Credit Limit:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9"))

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})

                    if htparam.fchar != "":
                        enter_passwd2 = True
                        htparam_fchar1 = htparam.fchar
                        guest_kreditlimit =  to_decimal(guest.kreditlimit)
                else:
                    msg_str2 = msg_str2 + chr_unicode(2) + "&Q" + translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9")) + chr_unicode(10) + translateExtended ("Cancel the C/L payment?", lvcarea, "")

    return generate_output()