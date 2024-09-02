from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy

def selforder_cek_payment_gatewaybl(session_parameter:str, outletno:int):
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


        return {"payment_status": payment_status, "payment_type": payment_type, "payment_date": payment_date, "trans_id_merchant": trans_id_merchant, "payment_channel": payment_channel, "result_message": result_message}

    def check_payment():

        nonlocal payment_status, payment_type, payment_date, trans_id_merchant, payment_channel, result_message, queasy

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 223) &  (Queasy.number1 == outletno) &  (func.lower(Queasy.char3) == (session_parameter).lower())).first()

        if queasy:
            payment_status = queasy.char1

            if queasy.number3 == 1:
                payment_type = "MIDTRANS"

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
            result_message = "0_Operation Success"
        else:
            result_message = "1_Data Not FOund"


    if outletno == None:
        outletno = 0

    if session_parameter == None:
        session_parameter = ""

    if session_parameter == "":
        result_message = "1_sessionParameter can't be Null"

        return generate_output()

    if outletno == 0:
        result_message = "2_outletno can't be set to 0"

        return generate_output()
    check_payment()

    if result_message.lower()  == "1_Data Not FOund":

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 223) &  (Queasy.number1 == outletno) &  (Queasy.betriebsnr == to_int(session_parameter))).first()

        if queasy:
            payment_status = queasy.char1

            if queasy.number3 == 1:
                payment_type = "MIDTRANS"

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
            result_message = "0_Operation Success"
        else:
            result_message = "1_Data Not FOund"

    return generate_output()