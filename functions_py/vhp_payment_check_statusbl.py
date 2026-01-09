# using conversion tools version: 1.0.0.119
"""_yusufwijasena_02/12/2025

    Ticket ID: 22F25D
        remark: - only converted to python 
        
    _yusufwijasena_09/01/2026
        remark: - deleted to_int in queasy.deci3 & queasy.deci2
"""
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy


def vhp_payment_check_statusbl(bill_number: int, rsv_number: int):

    prepare_cache([Queasy])

    result_message = ""
    payment_id = ""
    payment_channel = ""
    payment_method = ""
    payment_status = ""
    payment_amount = ""
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_message, payment_id, payment_channel, payment_method, payment_status, payment_amount, queasy
        nonlocal bill_number, rsv_number

        return {
            "result_message": result_message,
            "payment_id": payment_id,
            "payment_channel": payment_channel,
            "payment_method": payment_method,
            "payment_status": payment_status,
            "payment_amount": payment_amount
        }

    if bill_number == 0 and rsv_number != 0:
        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 372) &
                (Queasy.deci3 == rsv_number)
        ).order_by(
            Queasy.date1.desc(),
            Queasy.number3.desc()
        ).all():
            payment_id = queasy.char1
            payment_channel = entry(0, queasy.char3, "|")
            payment_method = entry(1, queasy.char3, "|")
            payment_status = queasy.char2
            payment_amount = to_string(queasy.deci1)
            break

        if payment_id == "":
            result_message = "No payment record was found!"

            return generate_output()

    elif bill_number != 0 and rsv_number == 0:
        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 372) &
                (Queasy.deci2 == bill_number)
        ).order_by(
            Queasy.date1.desc(),
            Queasy.number3.desc()
        ).all():
            payment_id = queasy.char1
            payment_channel = entry(0, queasy.char3, "|")
            payment_method = entry(1, queasy.char3, "|")
            payment_status = queasy.char2
            payment_amount = to_string(queasy.deci1)
            break

        if payment_id == "":
            result_message = "No payment record was found!"

            return generate_output()
    else:
        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 372) &
                (Queasy.deci2 == bill_number) &
                (Queasy.deci3 == rsv_number)
        ).order_by(
            Queasy.date1.desc(),
            Queasy.number3.desc()
        ).all():
            payment_id = queasy.char1
            payment_channel = entry(0, queasy.char3, "|")
            payment_method = entry(1, queasy.char3, "|")
            payment_status = queasy.char2
            payment_amount = to_string(queasy.deci1)
            break

        if payment_id == "":
            result_message = "No payment record was found!"

            return generate_output()
    result_message = "Check Status Success"

    return generate_output()
