from functions.additional_functions import *
import decimal
from models import Reservation

def read_reservationbl(case_type:int, rsvno:int, gastno:int, voucherno:str):
    t_reservation_list = []
    reservation = None

    t_reservation = None

    t_reservation_list, T_reservation = create_model_like(Reservation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_reservation_list, reservation


        nonlocal t_reservation
        nonlocal t_reservation_list
        return {"t-reservation": t_reservation_list}

    if case_type == 1:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == rsvno)).first()

        if reservation:
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)
    elif case_type == 2:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == rsvno and Reservation.gastnr == gastno)).first()

        if reservation:
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)
    elif case_type == 3:

        reservation = db_session.query(Reservation).filter(
                (Reservation.activeflag == 0) &  (Reservation.vesrdepot == voucherno)).first()

        if reservation:
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)
    elif case_type == 4:

        reservation = db_session.query(Reservation).filter(
                (Reservation.activeflag == 0) &  (Reservation.gastnr > 0)).first()

        if reservation:
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)
    elif case_type == 5:

        for reservation in db_session.query(Reservation).filter(
                (Reservation.name == voucherno) &  (Reservation.gastnr == gastno) &  (Reservation.activeflag == 0)).all():
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)
    elif case_type == 6:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resart == rsvno)).first()

        if reservation:
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)
    elif case_type == 7:

        reservation = db_session.query(Reservation).filter(
                (Reservation.activeflag == rsvno) &  (Reservation.guestnrcom[1] == gastno)).first()

        if reservation:
            t_reservation = T_reservation()
            t_reservation_list.append(t_reservation)

            buffer_copy(reservation, t_reservation)

    return generate_output()