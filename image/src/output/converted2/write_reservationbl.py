#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Reservation, Res_line

t_reservation_list, T_reservation = create_model_like(Reservation)

def write_reservationbl(case_type:int, resno:int, t_reservation_list:[T_reservation]):
    success_flag = False
    deposit:Decimal = to_decimal("0.0")
    deposit_pay1:Decimal = to_decimal("0.0")
    deposit_pay2:Decimal = to_decimal("0.0")
    reservation = res_line = None

    t_reservation = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, deposit, deposit_pay1, deposit_pay2, reservation, res_line
        nonlocal case_type, resno


        nonlocal t_reservation

        return {"success_flag": success_flag}

    def delete_procedure():

        nonlocal success_flag, deposit, deposit_pay1, deposit_pay2, reservation, res_line
        nonlocal case_type, resno


        nonlocal t_reservation

    if case_type == 1:

        t_reservation = query(t_reservation_list, first=True)

        reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

        if reservation:
            buffer_copy(t_reservation, reservation)
            pass
            pass
            success_flag = True


    elif case_type == 2:

        reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

        if reservation:
            success_flag = True


    elif case_type == 3:

        reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

        if reservation:
            db_session.delete(reservation)
            success_flag = True


    elif case_type == 4:

        t_reservation = query(t_reservation_list, first=True)

        if t_reservation:
            reservation = Reservation()
            db_session.add(reservation)

            buffer_copy(t_reservation, reservation)
            pass
            success_flag = True
    elif case_type == 5:

        reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

        if reservation:
            reservation.activeflag = 0
            pass
            success_flag = True
    elif case_type == 6:

        reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

        if reservation:
            reservation.verstat = 1
            pass
            success_flag = True
    elif case_type == 7:

        reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

        if reservation:
            reservation.verstat = 0
            pass
            success_flag = True
    elif case_type == 8:

        t_reservation = query(t_reservation_list, first=True)

        reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

        if reservation:
            buffer_copy(t_reservation, reservation)
            deposit =  to_decimal(reservation.depositgef)
            deposit_pay1 =  to_decimal(reservation.depositbez)
            deposit_pay2 =  to_decimal(reservation.depositbez2)

            if (- deposit_pay1 - deposit_pay2) > deposit:
                reservation.depositgef =  - to_decimal(deposit_pay1) - to_decimal(deposit_pay2)


            pass
            pass
            success_flag = True


    elif case_type == 9:

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)]})

        if not res_line:

            reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

            if reservation:
                db_session.delete(reservation)
                success_flag = True

    return generate_output()