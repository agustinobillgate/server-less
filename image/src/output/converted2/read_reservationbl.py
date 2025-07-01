#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Reservation

def read_reservationbl(case_type:int, rsvno:int, gastno:int, voucherno:string):
    t_reservation_list = []
    reservation = None

    t_reservation = None

    t_reservation_list, T_reservation = create_model_like(Reservation)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_reservation_list, reservation
        nonlocal case_type, rsvno, gastno, voucherno


        nonlocal t_reservation
        nonlocal t_reservation_list

        return {"t-reservation": t_reservation_list}

    if case_type == 1:

        reservation = get_cache (Reservation, {"resnr": [(eq, rsvno)]})

        if reservation:
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)
    elif case_type == 2:

        reservation = get_cache (Reservation, {"resnr": [(eq, rsvno)],"gastnr": [(eq, gastno)]})

        if reservation:
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)
    elif case_type == 3:

        reservation = get_cache (Reservation, {"activeflag": [(eq, 0)],"vesrdepot": [(eq, voucherno)]})

        if reservation:
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)
    elif case_type == 4:

        reservation = get_cache (Reservation, {"activeflag": [(eq, 0)],"gastnr": [(gt, 0)]})

        if reservation:
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)
    elif case_type == 5:

        for reservation in db_session.query(Reservation).filter(
                 (Reservation.name == voucherno) & (Reservation.gastnr == gastno) & (Reservation.activeflag == 0)).order_by(Reservation._recid).all():
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)
    elif case_type == 6:

        reservation = get_cache (Reservation, {"resart": [(eq, rsvno)]})

        if reservation:
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)
    elif case_type == 7:

        reservation = get_cache (Reservation, {"activeflag": [(eq, rsvno)],"guestnrcom[1]": [(eq, gastno)]})

        if reservation:
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)

    return generate_output()