from functions.additional_functions import *
import decimal
from models import Reservation

def quick_resline_check_depositbl(case_type:int, resnr:int, gastnr:int, deposit:decimal):
    flag1 = False
    reservation = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag1, reservation


        return {"flag1": flag1}


    if case_type == 1:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resnr) &  (Reservation.gastnr == gastnr)).first()
        reservation.depositgef = deposit

        reservation = db_session.query(Reservation).first()

    elif case_type == 2:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resnr) &  (Reservation.gastnr == gastnr)).first()

        if (reservation.depositbez == 0) and (reservation.depositbez2 == 0):
            flag1 = True

            return generate_output()