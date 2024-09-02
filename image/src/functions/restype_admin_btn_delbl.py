from functions.additional_functions import *
import decimal
from models import Reservation, Sourccod

def restype_admin_btn_delbl(source_code:int):
    flag = False
    success_flag = False
    reservation = sourccod = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, success_flag, reservation, sourccod


        return {"flag": flag, "success_flag": success_flag}


    reservation = db_session.query(Reservation).filter(
            (Reservation.resart == source_code)).first()

    if reservation:
        flag = True
    else:

        sourccod = db_session.query(Sourccod).filter(
                (Sourccod.source_code == source_code)).first()
        db_session.delete(sourccod)
        success_flag = True

    return generate_output()