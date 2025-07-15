#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Ratecode, Guest, Htparam, Guest_pr, Queasy, Guestseg, Segment, Artikel, Debitor, Reservation, Res_line

def reservation_btn_newbl(i_case:int, pvilanguage:int, gastnr:int):

    prepare_cache ([Ratecode, Htparam, Segment, Debitor, Reservation, Res_line])

    msg_str = ""
    error_flag = True
    pswd_str = ""
    outstand = to_decimal("0.0")
    resno = 0
    lvcarea:string = "reservation"
    ratecode_exist:bool = False
    bill_date:date = None
    static_rcode:string = ""
    ratecode = guest = htparam = guest_pr = queasy = guestseg = segment = artikel = debitor = reservation = res_line = None

    rcbuff = None

    Rcbuff = create_buffer("Rcbuff",Ratecode)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_flag, pswd_str, outstand, resno, lvcarea, ratecode_exist, bill_date, static_rcode, ratecode, guest, htparam, guest_pr, queasy, guestseg, segment, artikel, debitor, reservation, res_line
        nonlocal i_case, pvilanguage, gastnr
        nonlocal rcbuff


        nonlocal rcbuff

        return {"msg_str": msg_str, "error_flag": error_flag, "pswd_str": pswd_str, "outstand": outstand, "resno": resno}

    def get_newresno():

        nonlocal msg_str, error_flag, pswd_str, outstand, resno, lvcarea, ratecode_exist, bill_date, static_rcode, ratecode, guest, htparam, guest_pr, queasy, guestseg, segment, artikel, debitor, reservation, res_line
        nonlocal i_case, pvilanguage, gastnr
        nonlocal rcbuff


        nonlocal rcbuff

        resno = 0
        rline = None

        def generate_inner_output():
            return (resno)

        Rline =  create_buffer("Rline",Res_line)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 736)]})

        if htparam.fchar != "":
            resno = get_output(run_program(htparam.fchar,()))
        else:

            reservation = db_session.query(Reservation).first()

            if not reservation:
                resno = 1
            else:
                resno = reservation.resnr + 1

        for rline in db_session.query(Rline).order_by(Rline.resnr.desc()).all():

            if resno <= rline.resnr:
                resno = rline.resnr + 1
            break

        return generate_inner_output()


    bill_date = get_output(htpdate(110))

    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 735)]})

    if htparam.feldtyp == 4 and htparam.flogical:

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, gastnr)]})
        while None != guest_pr:

            queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, guest_pr.code)]})

            if queasy.logi2:

                for rcbuff in db_session.query(Rcbuff).filter(
                         (Rcbuff.code == guest_pr.code)).order_by(Rcbuff._recid).yield_per(100):

                    ratecode = get_cache (Ratecode, {"code": [(eq, substring(entry(7, rcbuff.char1[4], ";") , 2))],"endperiode": [(ge, bill_date)]})

                    if ratecode:
                        ratecode_exist = True
                        break
            else:

                ratecode = get_cache (Ratecode, {"code": [(eq, guest_pr.code)],"endperiode": [(ge, bill_date)]})

                if ratecode:
                    ratecode_exist = True
                    break

            curr_recid = guest_pr._recid
            guest_pr = db_session.query(Guest_pr).filter(
                     (Guest_pr.gastnr == gastnr) & (Guest_pr._recid > curr_recid)).first()

        if not ratecode_exist:
            msg_str = translateExtended ("Rate code not found or expired.", lvcarea, "")
            error_flag = True

            return generate_output()

    if i_case == 1:

        guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)]})
        while None != guestseg:

            segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)],"betriebsnr": [(eq, 4)]})

            if segment:

                if guest.zahlungsart > 0:

                    debitor_obj_list = {}
                    for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 7))).filter(
                             (Debitor.gastnr == guest.gastnr) & (Debitor.opart <= 1)).order_by(Debitor._recid).all():
                        if debitor_obj_list.get(debitor._recid):
                            continue
                        else:
                            debitor_obj_list[debitor._recid] = True


                        outstand =  to_decimal(outstand) + to_decimal(debitor.saldo)


                htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})

                if htparam.fchar != "":
                    pswd_str = htparam.fchar
                    msg_str = translateExtended ("Black List:", lvcarea, "") +\
                        " " + entry(0, segment.bezeich, "$$0")


                else:
                    msg_str = "&Q" + translateExtended ("Black List:", lvcarea, "") + " " + entry(0, segment.bezeich, "$$0") + chr_unicode(10) + translateExtended ("Cancel Booking?", lvcarea, "")

                return generate_output()

            curr_recid = guestseg._recid
            guestseg = db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == guest.gastnr) & (Guestseg._recid > curr_recid)).first()

        if guest.kreditlimit > 0 and guest.zahlungsart > 0:

            debitor_obj_list = {}
            for debitor, artikel in db_session.query(Debitor, Artikel).join(Artikel,(Artikel.artnr == Debitor.artnr) & (Artikel.departement == 0) & (Artikel.artart == 2)).filter(
                     (Debitor.gastnr == guest.gastnr) & (Debitor.opart <= 1)).order_by(Debitor._recid).all():
                if debitor_obj_list.get(debitor._recid):
                    continue
                else:
                    debitor_obj_list[debitor._recid] = True


                outstand =  to_decimal(outstand) + to_decimal(debitor.saldo)

            if outstand > guest.kreditlimit:

                htparam = get_cache (Htparam, {"paramnr": [(eq, 320)]})

                if htparam.flogical:
                    msg_str = translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9"))

                    return generate_output()
                else:
                    msg_str = "&Q" + translateExtended ("Credit Limit overdrawn:", lvcarea, "") + " " + trim(to_string(outstand, "->,>>>,>>>,>>>,>>9")) + " >> " + trim(to_string(guest.kreditlimit, "->>>,>>>,>>>,>>9")) + chr_unicode(10) + translateExtended ("Cancel creating new reservation?", lvcarea, "")

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


    pass
    pass

    return generate_output()