#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Reservation, Htparam, Segment, Guestseg, Res_line

def get_dynarates_bookingbl(wi_flag:bool, gastno:int, resno:int):

    prepare_cache ([Reservation, Htparam, Res_line])

    segm_ok:bool = True
    guest = reservation = htparam = segment = guestseg = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal segm_ok, guest, reservation, htparam, segment, guestseg, res_line
        nonlocal wi_flag, gastno, resno

        return {"resno": resno}

    def check_walkin_segm():

        nonlocal segm_ok, guest, reservation, htparam, segment, guestseg, res_line
        nonlocal wi_flag, gastno, resno

        wi_segm:bool = False
        main_exist:bool = False
        segmstr:string = ""
        curr_segm:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 48)]})

        if htparam.finteger != 0:

            segment = get_cache (Segment, {"segmentcode": [(eq, htparam.finteger)]})
            wi_segm = None != segment

        if not wi_segm:
            segm_ok = False

            return
        curr_segm = segment.segmentcode

        guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})

        guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"segmentcode": [(eq, curr_segm)]})

        if not guestseg:

            guestseg = get_cache (Guestseg, {"gastnr": [(eq, guest.gastnr)],"reihenfolge": [(eq, 1)]})
            main_exist = None != guestseg
            guestseg = Guestseg()
            db_session.add(guestseg)

            guestseg.gastnr = guest.gastnr
            guestseg.segmentcode = curr_segm

            if not main_exist:
                guestseg.reihenfolge = 1


    def get_newresno():

        nonlocal segm_ok, guest, reservation, htparam, segment, guestseg, res_line
        nonlocal wi_flag, gastno, resno

        resno = 0

        def generate_inner_output():
            return (resno)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 736)]})

        if htparam.fchar != "":
            resno = get_output(run_program(htparam.fchar,()))
        else:

            reservation = db_session.query(Reservation).first()

            if not reservation:
                resno = 1
            else:
                resno = reservation.resnr + 1

        for res_line in db_session.query(Res_line).order_by(Res_line.resnr.desc()).yield_per(100):

            if resno <= res_line.resnr:
                resno = res_line.resnr + 1
            break

        return generate_inner_output()

    if wi_flag:
        check_walkin_segm()

        if not segm_ok:

            return generate_output()

    guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})

    if resno == 0:
        resno = get_newresno()
        reservation = Reservation()
        db_session.add(reservation)

        reservation.resnr = resno
        reservation.name = guest.name


        pass
        pass

    return generate_output()