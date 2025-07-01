#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Reservation, Res_line

def assign_anzahlbl(resnr:int):

    prepare_cache ([Reservation])

    anzahl = 0
    deposit:bool = False
    reservation = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anzahl, deposit, reservation, res_line
        nonlocal resnr

        return {"anzahl": anzahl}


    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    if (reservation.depositbez + reservation.depositbez2) != 0:
        deposit = True

    if deposit:

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.resnr == resnr) & (Res_line.active_flag == 0)).order_by(Res_line._recid).all():
            anzahl = anzahl + 1

    return generate_output()