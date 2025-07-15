#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htpchar import htpchar
from models import Reservation, Res_line

def get_newresnobl():

    prepare_cache ([Reservation, Res_line])

    resno = 0
    progname:string = ""
    reservation = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resno, progname, reservation, res_line

        return {"resno": resno}

    progname = get_output(htpchar(736))

    if progname != "":
        resno = get_output(run_program(progname,()))
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

    return generate_output()