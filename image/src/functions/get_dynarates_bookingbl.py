from functions.additional_functions import *
import decimal
from models import Guest, Reservation, Htparam, Segment, Guestseg, Res_line

def get_dynarates_bookingbl(wi_flag:bool, gastno:int, resno:int):
    segm_ok:bool = True
    guest = reservation = htparam = segment = guestseg = res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal segm_ok, guest, reservation, htparam, segment, guestseg, res_line


        return {}

    def check_walkin_segm():

        nonlocal segm_ok, guest, reservation, htparam, segment, guestseg, res_line

        wi_segm:bool = False
        main_exist:bool = False
        segmstr:str = ""
        curr_segm:int = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 48)).first()

        if htparam.finteger != 0:

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == htparam.finteger)).first()
            wi_segm = None != segment

        if not wi_segm:
            segm_ok = False

            return
        curr_segm = segmentcode

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == gastno)).first()

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == guest.gastnr) &  (Guestseg.segmentcode == curr_segm)).first()

        if not guestseg:

            guestseg = db_session.query(Guestseg).filter(
                    (Guestseg.gastnr == guest.gastnr) &  (Guestseg.reihenfolge == 1)).first()
            main_exist = None != guestseg
            guestseg = Guestseg()
            db_session.add(guestseg)

            guestseg.gastnr = guest.gastnr
            guestseg.segmentcode = curr_segm

            if not main_exist:
                guestseg.reihenfolge = 1

    def get_newresno():

        nonlocal segm_ok, guest, reservation, htparam, segment, guestseg, res_line

        resno = 0

        def generate_inner_output():
            return resno

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

        for res_line in db_session.query(Res_line).all():

            if resno <= res_line.resnr:
                resno = res_line.resnr + 1
            break


        return generate_inner_output()


    if wi_flag:
        check_walkin_segm()

        if not segm_ok:

            return generate_output()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastno)).first()

    if resno == 0:
        resno = get_newresno()
        reservation = Reservation()
        db_session.add(reservation)

        reservation.resnr = resno
        reservation.name = guest.name

        reservation = db_session.query(Reservation).first()


    return generate_output()