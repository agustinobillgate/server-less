from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Ratecode, Guest, Htparam, Guest_pr, Queasy, Guestseg, Segment, Artikel, Debitor, Reservation, Res_line

def reservation_btn_newbl(i_case:int, pvilanguage:int, gastnr:int):
    msg_str = ""
    error_flag = False
    pswd_str = ""
    outstand = 0
    resno = 0
    lvcarea:str = "reservation"
    ratecode_exist:bool = False
    bill_date:date = None
    static_rcode:str = ""
    ratecode = guest = htparam = guest_pr = queasy = guestseg = segment = artikel = debitor = reservation = res_line = None

    rcbuff = rline = None

    Rcbuff = Ratecode
    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_flag, pswd_str, outstand, resno, lvcarea, ratecode_exist, bill_date, static_rcode, ratecode, guest, htparam, guest_pr, queasy, guestseg, segment, artikel, debitor, reservation, res_line
        nonlocal rcbuff, rline


        nonlocal rcbuff, rline
        return {"msg_str": msg_str, "error_flag": error_flag, "pswd_str": pswd_str, "outstand": outstand, "resno": resno}

    def get_newresno():

        nonlocal msg_str, error_flag, pswd_str, outstand, resno, lvcarea, ratecode_exist, bill_date, static_rcode, ratecode, guest, htparam, guest_pr, queasy, guestseg, segment, artikel, debitor, reservation, res_line
        nonlocal rcbuff, rline


        nonlocal rcbuff, rline

        resno = 0

        def generate_inner_output():
            return resno
        Rline = Res_line

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 736)).first()

        if htparam.fchar != "":
            htparam.fchar) (resno = value(htparam.fchar) (resno)
        else:

            reservation = db_session.query(Reservation).first()

            if not reservation:
                resno = 1
            else:
                resno = reservation.resnr + 1

        for rline in db_session.query(Rline).all():

            if resno <= rline.resnr:
                resno = rline.resnr + 1
            break


        return generate_inner_output()

    bill_date = get_output(htpdate(110))

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastnr)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 735)).first()

    if htparam.feldtyp == 4 and htparam.flogical:

        guest_pr = db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == gastnr)).first()
        while None != guest_pr:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 2) &  (Queasy.char1 == guest_pr.CODE)).first()

            if queasy.logi2:

                for rcbuff in db_session.query(Rcbuff).filter(
                        (Rcbuff.CODE == guest_pr.CODE)).all():

                    ratecode = db_session.query(Ratecode).filter(
                            (Ratecode.CODE == substring(entry(7, rcbuff.char1[4], ";") , 2)) &  (Ratecode.endperiode >= bill_date)).first()

                    if ratecode:
                        ratecode_exist = True
                        break
            else:

                ratecode = db_session.query(Ratecode).filter(
                        (Ratecode.CODE == guest_pr.CODE) &  (Ratecode.endperiode >= bill_date)).first()

                if ratecode:
                    ratecode_exist = True
                    break

            guest_pr = db_session.query(Guest_pr).filter(
                    (Guest_pr.gastnr == gastnr)).first()

        if not ratecode_exist:
            msg_str = translateExtended ("Rate code not found or expired.", lvcarea, "")
            error_flag = True

            return generate_output()

    if i_case == 1:

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == guest.gastnr)).first()
        while None != guestseg:

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == guestseg.segmentcode) &  (Segment.betriebsnr == 4)).first()

            if segment:

                if guest.zahlungsart > 0:

                    debitor_obj_list = []
                    for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.departement == 0) &  ((Artikel.artart == 2) |  (Artikel.artart == 7))).filter(
                            (Debitor.gastnr == guest.gastnr) &  (Debitor.opart <= 1)).all():
                        if debitor._recid in debitor_obj_list:
                            continue
                        else:
                            debitor_obj_list.append(debitor._recid)


                        outstand = outstand + debitor.saldo


                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 141)).first()

                if htparam.fchar != "":
                    pswd_str = htparam.fchar
                    msg_str = translateExtended ("Black List:", lvcarea, "") +\
                        " " + entry(0, segment.bezeich, "$$0")


                else:
                    msg_str = "&Q" + translateExtended ("Black List:", lvcarea, "") + " " + entry(0, segment.bezeich, "$$0") + chr(10) + translateExtended ("Cancel Booking?", lvcarea, "")

                return generate_output()

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == guest.gastnr)).first()

        if guest.kreditlimit > 0 and guest.zahlungsart > 0:

            debitor_obj_list = []
            for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) &  (Artikel.departement == 0) &  (Artikel.artart == 2)).filter(
                    (Debitor.gastnr == guest.gastnr) &  (Debitor.opart <= 1)).all():
                if debitor._recid in debitor_obj_list:
                    continue
                else:
                    debitor_obj_list.append(debitor._recid)


                outstand = outstand + debitor.saldo

            if outstand > guest.kreditlimit:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 320)).first()

                if htparam.flogical:
                    msg_str = translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9"))

                    return generate_output()
                else:
                    msg_str = "&Q" + translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9")) + chr(10) + translateExtended ("Cancel creating new reservation?", lvcarea, "")

                    return generate_output()
    error_flag = False
    resno = get_newresno()
    reservation = Reservation()
    db_session.add(reservation)

    reservation.resnr = resno
    reservation.gastnr = gastnr
    reservation.gastnrherk = gastnr
    reservation.name = guest.name
    reservation.herkunft = guest.name + ", " + guest.vorname1 +\
            guest.anredefirma

    reservation = db_session.query(Reservation).first()


    return generate_output()