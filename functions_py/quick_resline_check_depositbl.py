#using conversion tools version: 1.0.0.117
#==========================================================
# Rd, 25/11/2025, with_for_update(), tidak ada excl-lock
#==========================================================
from functions.additional_functions import *
from decimal import Decimal
from models import Reservation

def quick_resline_check_depositbl(case_type:int, resnr:int, gastnr:int, deposit:Decimal):

    prepare_cache ([Reservation])

    flag1 = False
    reservation = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag1, reservation
        nonlocal case_type, resnr, gastnr, deposit

        return {"flag1": flag1}


    if case_type == 1:

        # reservation = get_cache (Reservation, {"resnr": [(eq, resnr)],"gastnr": [(eq, gastnr)]})
        reservation = db_session.query(Reservation).filter(Reservation.resnr == resnr, Reservation.gastnr == gastnr).with_for_update().first()
        reservation.depositgef =  to_decimal(deposit)

        pass

    elif case_type == 2:

        reservation = get_cache (Reservation, {"resnr": [(eq, resnr)],"gastnr": [(eq, gastnr)]})

        if (reservation.depositbez == 0) and (reservation.depositbez2 == 0):
            flag1 = True

            return generate_output()

    return generate_output()