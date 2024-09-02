from functions.additional_functions import *
import decimal
from models import Reservation, Res_line

def write_reservationbl(case_type:int, resno:int, t_reservation:[T_reservation]):
    success_flag = False
    deposit:decimal = 0
    deposit_pay1:decimal = 0
    deposit_pay2:decimal = 0
    reservation = res_line = None

    t_reservation = None

    t_reservation_list, T_reservation = create_model_like(Reservation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, deposit, deposit_pay1, deposit_pay2, reservation, res_line


        nonlocal t_reservation
        nonlocal t_reservation_list
        return {"success_flag": success_flag}

    def delete_procedure():

        nonlocal success_flag, deposit, deposit_pay1, deposit_pay2, reservation, res_line


        nonlocal t_reservation
        nonlocal t_reservation_list

    hHandle = THIS_PROCEDURE

    if case_type == 1:

        t_reservation = query(t_reservation_list, first=True)

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()

        if reservation:
            buffer_copy(t_reservation, reservation)

            reservation = db_session.query(Reservation).first()

            success_flag = True


    elif case_type == 2:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()

        if reservation:
            success_flag = True


    elif case_type == 3:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()

        if reservation:
            db_session.delete(reservation)
            success_flag = True


    elif case_type == 4:

        t_reservation = query(t_reservation_list, first=True)

        if t_reservation:
            reservation = Reservation()
            db_session.add(reservation)

            buffer_copy(t_reservation, reservation)

            reservation = db_session.query(Reservation).first()
            success_flag = True
    elif case_type == 5:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()

        if reservation:
            reservation.activeflag = 0

            reservation = db_session.query(Reservation).first()
            success_flag = True
    elif case_type == 6:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()

        if reservation:
            reservation.verstat = 1

            reservation = db_session.query(Reservation).first()
            success_flag = True
    elif case_type == 7:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()

        if reservation:
            reservation.verstat = 0

            reservation = db_session.query(Reservation).first()
            success_flag = True
    elif case_type == 8:

        t_reservation = query(t_reservation_list, first=True)

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()

        if reservation:
            buffer_copy(t_reservation, reservation)
            deposit = reservation.depositgef
            deposit_pay1 = reservation.depositbez
            deposit_pay2 = reservation.depositbez2

            if (- deposit_pay1 - deposit_pay2) > deposit:
                reservation.depositgef = - deposit_pay1 - deposit_pay2

            reservation = db_session.query(Reservation).first()

            success_flag = True


    elif case_type == 9:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno)).first()

        if not res_line:

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == resno)).first()

            if reservation:
                db_session.delete(reservation)
                success_flag = True

    return generate_output()