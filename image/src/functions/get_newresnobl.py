from functions.additional_functions import *
import decimal
from functions.htpchar import htpchar
from models import Reservation, Res_line

def get_newresnobl():
    resno = 0
    progname:str = ""
    reservation = res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resno, progname, reservation, res_line


        return {"resno": resno}

    progname = get_output(htpchar(736))

    if progname != "":
        progname) (resno = value(progname) (resno)
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

    return generate_output()