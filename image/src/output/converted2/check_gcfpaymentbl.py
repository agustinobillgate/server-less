from functions.additional_functions import *
import decimal
from models import Artikel, Htparam, Guest, Debitor

def check_gcfpaymentbl(pvilanguage:int, gastnr:int, payment:int):
    msg_str = ""
    msg_str2 = ""
    htparam_fchar = ""
    htparam_fchar1 = ""
    guest_kreditlimit = to_decimal("0.0")
    enter_passwd1 = False
    enter_passwd2 = False
    lvcarea:str = "check-gcfpayment"
    zahlungsart:int = 0
    outstand:decimal = to_decimal("0.0")
    artikel = htparam = guest = debitor = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, htparam_fchar, htparam_fchar1, guest_kreditlimit, enter_passwd1, enter_passwd2, lvcarea, zahlungsart, outstand, artikel, htparam, guest, debitor
        nonlocal pvilanguage, gastnr, payment


        return {"payment": payment, "msg_str": msg_str, "msg_str2": msg_str2, "htparam_fchar": htparam_fchar, "htparam_fchar1": htparam_fchar1, "guest_kreditlimit": guest_kreditlimit, "enter_passwd1": enter_passwd1, "enter_passwd2": enter_passwd2}


    artikel = db_session.query(Artikel).filter(
             (Artikel.artnr == payment) & (Artikel.departement == 0)).first()

    if artikel and artikel.artart == 2:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 116)).first()

        if artikel.zwkum == htparam.finteger:

            return generate_output()

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == gastnr)).first()

        if guest:
            zahlungsart = guest.zahlungsart

        if zahlungsart == 0:

            htparam = db_session.query(Htparam).filter(
                     (Htparam.paramnr == 141)).first()

            if htparam.fchar != "":
                enter_passwd1 = True
                htparam_fchar = htparam.fchar
            else:
                msg_str = msg_str + chr(2) + "&W" + translateExtended ("No C/L payment Articles have been defined for this Guest.", lvcarea, "")

        elif guest.zahlungsart != payment:

            artikel = db_session.query(Artikel).filter(
                     (Artikel.departement == 0) & (Artikel.artnr == guest.zahlungsart)).first()

            if artikel:
                msg_str = msg_str + chr(2) + translateExtended ("C/L payment Article for this guest is", lvcarea, "") + chr(10) + to_string(artikel.artnr) + " - " + artikel.bezeich
                payment = 0

                return generate_output()

        if guest.karteityp >= 1 and guest.kreditlimit > 0:

            debitor_obj_list = []
            for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).filter(
                     (Debitor.gastnr == guest.gastnr) & (Debitor.opart <= 1)).order_by(Debitor._recid).all():
                if debitor._recid in debitor_obj_list:
                    continue
                else:
                    debitor_obj_list.append(debitor._recid)


                outstand =  to_decimal(outstand) + to_decimal(debitor.saldo)

            if outstand > guest.kreditlimit:

                htparam = db_session.query(Htparam).filter(
                         (Htparam.paramnr == 320)).first()

                if htparam.flogical:
                    msg_str2 = msg_str2 + chr(2) + translateExtended ("Over Credit Limit:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9"))

                    htparam = db_session.query(Htparam).filter(
                             (Htparam.paramnr == 141)).first()

                    if htparam.fchar != "":
                        enter_passwd2 = True
                        htparam_fchar1 = htparam.fchar
                        guest_kreditlimit =  to_decimal(guest.kreditlimit)
                else:
                    msg_str2 = msg_str2 + chr(2) + "&Q" + translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9")) + chr(10) + translateExtended ("Cancel the C/L payment?", lvcarea, "")

    return generate_output()