#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def selforder_cek_payment_gatewaybl(session_parameter:string, outletno:int):

    prepare_cache ([Queasy])

    payment_status = ""
    payment_type = ""
    payment_date = None
    trans_id_merchant = ""
    payment_channel = ""
    result_message = ""
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal payment_status, payment_type, payment_date, trans_id_merchant, payment_channel, result_message, queasy
        nonlocal session_parameter, outletno

        return {"payment_status": payment_status, "payment_type": payment_type, "payment_date": payment_date, "trans_id_merchant": trans_id_merchant, "payment_channel": payment_channel, "result_message": result_message}

    def check_payment():

        nonlocal payment_status, payment_type, payment_date, trans_id_merchant, payment_channel, result_message, queasy
        nonlocal session_parameter, outletno

        queasy = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, outletno)],"char3": [(eq, session_parameter)]})

        if queasy:
            payment_status = queasy.char1

            if queasy.number3 == 1:
                payment_type = "MIDtrans"

            elif queasy.number3 == 2:
                payment_type = "DOKU"

            elif queasy.number3 == 3:
                payment_type = "QRIS"

            elif queasy.number3 == 4:
                payment_type = "XENDIT"
            payment_date = queasy.date1

            if num_entries(queasy.char2, "|") > 2:
                payment_channel = entry(1, queasy.char2, "|")
                trans_id_merchant = entry(2, queasy.char2, "|")
                payment_type = entry(0, queasy.char2, "|")
            else:
                trans_id_merchant = queasy.char2
            result_message = "0-Operation Success"
        else:
            result_message = "1-Data Not FOund"

    if outletno == None:
        outletno = 0

    if session_parameter == None:
        session_parameter = ""

    if session_parameter == "":
        result_message = "1-sessionParameter can't be Null"

        return generate_output()

    if outletno == 0:
        result_message = "2-outletno can't be set to 0"

        return generate_output()
    check_payment()

    if result_message.lower()  == ("1-Data Not FOund").lower() :

        queasy = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, outletno)],"betriebsnr": [(eq, to_int(session_parameter))]})

        if queasy:
            payment_status = queasy.char1

            if queasy.number3 == 1:
                payment_type = "MIDtrans"

            elif queasy.number3 == 2:
                payment_type = "DOKU"

            elif queasy.number3 == 3:
                payment_type = "QRIS"

            elif queasy.number3 == 4:
                payment_type = "XENDIT"
            payment_date = queasy.date1

            if num_entries(queasy.char2, "|") > 2:
                payment_channel = entry(1, queasy.char2, "|")
                trans_id_merchant = entry(2, queasy.char2, "|")
                payment_type = entry(0, queasy.char2, "|")
            else:
                trans_id_merchant = queasy.char2
            result_message = "0-Operation Success"
        else:
            result_message = "1-Data Not FOund"

    return generate_output()