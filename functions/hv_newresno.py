from functions.additional_functions import *
import decimal
from models import Htparam, Reservation

def hv_newresno():
    resno = 0
    yy:int = 0
    htparam = reservation = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal resno, yy, htparam, reservation

        return {"resno": resno}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()
    yy = (get_year(htparam.fdate) - 2000) * 100000

    reservation = db_session.query(Reservation).filter(
             (Reservation.resnr >= yy)).first()

    if reservation:

        reservation = db_session.query(Reservation).first()
        resno = reservation.resnr + 1


    else:
        resno = yy + 1

    return generate_output()