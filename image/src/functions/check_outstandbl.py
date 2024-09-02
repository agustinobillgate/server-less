from functions.additional_functions import *
import decimal
from models import Guest, Segment, Guestseg, Artikel, Debitor, Htparam

def check_outstandbl(pvilanguage:int, gastnr:int, from_inv:bool):
    msg_str = ""
    error_flag = False
    pswd_str = ""
    outstand = 0
    black_list_flag:bool = False
    lvcarea:str = "reservation"
    guest = segment = guestseg = artikel = debitor = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_flag, pswd_str, outstand, black_list_flag, lvcarea, guest, segment, guestseg, artikel, debitor, htparam


        return {"msg_str": msg_str, "error_flag": error_flag, "pswd_str": pswd_str, "outstand": outstand}


    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    guestseg_obj_list = []
    for guestseg, segment in db_session.query(Guestseg, Segment).join(Segment,(Segment.segmentcode == Guestseg.segmentcode) &  (Segment.betriebsnr == 4)).filter(
            (Guestseg.gastnr == guest.gastnr)).all():
        if guestseg._recid in guestseg_obj_list:
            continue
        else:
            guestseg_obj_list.append(guestseg._recid)

        if guest.zahlungsart > 0:

            debitor_obj_list = []
            for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.departement == 0) &  ((Artikel.artart == 2) |  (Artikel.artart == 7))).filter(
                    (Debitor.gastnr == guest.gastnr) &  (Debitor.opart <= 1)).all():
                if debitor._recid in debitor_obj_list:
                    continue
                else:
                    debitor_obj_list.append(debitor._recid)


                outstand = outstand + debitor.saldo

        black_list_flag = True
        break

    if guest.karteityp >= 1 and guest.kreditlimit > 0 and guest.zahlungsart > 0:

        debitor_obj_list = []
        for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.departement == 0) &  (Artikel.artart == 2)).filter(
                (Debitor.gastnr == guest.gastnr) &  (Debitor.opart <= 1)).all():
            if debitor._recid in debitor_obj_list:
                continue
            else:
                debitor_obj_list.append(debitor._recid)


            outstand = outstand + debitor.saldo

        if outstand > guest.kreditlimit:

            if not from_inv:

                if black_list_flag:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 141)).first()

                    if htparam.fchar != "":
                        pswd_str = htparam.fchar
                        msg_str = translateExtended ("Black List:", lvcarea, "") +\
                            " " + entry(0, segment.bezeich, "$$0")


                    else:
                        msg_str = "&Q" + translateExtended ("Black List:", lvcarea, "") + " " + entry(0, segment.bezeich, "$$0") + chr(10) + translateExtended ("Cancel Booking?", lvcarea, "")
                else:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 320)).first()

                    if htparam.flogical:
                        msg_str = translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9"))

                        htparam = db_session.query(Htparam).filter(
                                (Htparam.paramnr == 141)).first()
                        pswd_str = htparam.fchar

                        return generate_output()
                    else:
                        msg_str = "&Q" + translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9")) + chr(10) + translateExtended ("Cancel creating new reservation?", lvcarea, "")

                        return generate_output()
            else:
                msg_str = translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9"))

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 141)).first()
                pswd_str = htparam.fchar

                return generate_output()
    error_flag = False

    return generate_output()