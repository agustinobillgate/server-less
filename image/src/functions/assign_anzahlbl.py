from functions.additional_functions import *
import decimal
from models import Reservation, Res_line

def assign_anzahlbl(resnr:int):
    anzahl = 0
    deposit:bool = False
    reservation = res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal anzahl, deposit, reservation, res_line


        return {"anzahl": anzahl}


    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()

    if (reservation.depositbez + reservation.depositbez2) != 0:
        deposit = True

    if deposit:

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == resnr) &  (Res_line.active_flag == 0)).all():
            anzahl = anzahl + 1

    return generate_output()