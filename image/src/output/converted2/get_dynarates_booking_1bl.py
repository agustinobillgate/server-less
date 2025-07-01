#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Guest, Reservation, Htparam, Segment, Guestseg, Res_line

def get_dynarates_booking_1bl(wi_flag:bool, gastno:int, repeat_charge:bool, every_month:int, repeat_amount:Decimal, start_date:date, end_date:date, resno:int):

    prepare_cache ([Queasy, Reservation, Htparam, Res_line])

    segm_ok:bool = True
    queasy = guest = reservation = htparam = segment = guestseg = res_line = None

    bqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal segm_ok, queasy, guest, reservation, htparam, segment, guestseg, res_line
        nonlocal wi_flag, gastno, repeat_charge, every_month, repeat_amount, start_date, end_date, resno
        nonlocal bqueasy


        nonlocal bqueasy

        return {"resno": resno}

    def update_repeat_charge():

        nonlocal segm_ok, queasy, guest, reservation, htparam, segment, guestseg, res_line
        nonlocal wi_flag, gastno, repeat_charge, every_month, repeat_amount, start_date, end_date, resno
        nonlocal bqueasy


        nonlocal bqueasy

        bqueasy = get_cache (Queasy, {"key": [(eq, 301)],"number1": [(eq, resno)]})

        if not bqueasy:
            bqueasy = Queasy()
            db_session.add(bqueasy)

            bqueasy.key = 301
            bqueasy.number1 = resno
            bqueasy.number2 = every_month
            bqueasy.deci1 =  to_decimal(repeat_amount)
            bqueasy.date1 = start_date
            bqueasy.date2 = end_date
            bqueasy.char1 = "$$"
            bqueasy.date3 = get_current_date()
            bqueasy.number3 = get_current_time_in_seconds()
            bqueasy.logi1 = repeat_charge


        else:
            pass
            bqueasy.logi1 = repeat_charge
            bqueasy.number2 = every_month
            bqueasy.deci1 =  to_decimal(repeat_amount)
            bqueasy.date1 = start_date
            bqueasy.date2 = end_date
            bqueasy.char1 = "$$"
            bqueasy.date3 = get_current_date()
            bqueasy.number3 = get_current_time_in_seconds()


            pass
            pass


    def check_walkin_segm():

        nonlocal segm_ok, queasy, guest, reservation, htparam, segment, guestseg, res_line
        nonlocal wi_flag, gastno, repeat_charge, every_month, repeat_amount, start_date, end_date, resno
        nonlocal bqueasy


        nonlocal bqueasy

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

        nonlocal segm_ok, queasy, guest, reservation, htparam, segment, guestseg, res_line
        nonlocal wi_flag, gastno, repeat_charge, every_month, repeat_amount, start_date, end_date, resno
        nonlocal bqueasy


        nonlocal bqueasy

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

    if repeat_charge:
        update_repeat_charge()

    return generate_output()