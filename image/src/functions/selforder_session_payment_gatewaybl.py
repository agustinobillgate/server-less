from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def selforder_session_payment_gatewaybl(session_parameter:str, trans_id_merchant:str, outletno:int, payment_type:int, payment_channel:str):
    trans_status = ""
    result_message = ""
    paymentmethod:str = ""
    paymentcode:int = 0
    queasy = None

    bqsy = None

    Bqsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal trans_status, result_message, paymentmethod, paymentcode, queasy
        nonlocal bqsy


        nonlocal bqsy
        return {"trans_status": trans_status, "result_message": result_message}


    if trans_id_merchant == None:
        trans_id_merchant = ""

    if payment_type == None:
        payment_type = 0

    if outletno == None:
        outletno = 0

    if session_parameter == None:
        session_parameter = ""

    if payment_channel == None:
        payment_channel = ""

    if trans_id_merchant == "":
        result_message = "1_Transaction Id Merchant can't be Null"

        return generate_output()

    if payment_type == 1:
        paymentmethod = "MIDTRANS"
        paymentcode = 1

    elif payment_type == 2:
        paymentmethod = "DOKU"
        paymentcode = 2

    elif payment_type == 3:
        paymentmethod = "QRIS"
        paymentcode = 3

    elif payment_type == 4:
        paymentmethod = "XENDIT"
        paymentcode = 4


    else:
        result_message = "2_Wrong Case Type should be 1 == MIDTRANS, 2 == QRIS, 3 == DOKU, 4 == XENDIT"

        return generate_output()

    if session_parameter == "":
        result_message = "3_sessionParameter can't be Null"

        return generate_output()

    if outletno == 0:
        result_message = "4_outletno can't be set to 0"

        return generate_output()

    if payment_channel == "":
        result_message = "5_paymentChannel can't be Null"

        return generate_output()
    trans_status = "PENDING"

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 223) &  (Queasy.number1 == outletno) &  (func.lower(Queasy.char3) == (session_parameter).lower())).first()

    if queasy:

        queasy = db_session.query(Queasy).first()
        queasy.char1 = trans_status
        queasy.char2 = paymentmethod + "|" + payment_channel + "|" + trans_id_merchant
        queasy.date1 = get_current_date()


        result_message = "0_Operation Success"
        trans_status = queasy.char1 + " transID == " + queasy.char2

        queasy = db_session.query(Queasy).first()

    else:

        bqsy = db_session.query(Bqsy).filter(
                (Bqsy.key == 223) &  (Bqsy.number1 == outletno) &  (Bqsy.betriebsnr == to_int(session_parameter))).first()

        if bqsy:

            bqsy = db_session.query(Bqsy).first()
            bqsy.char1 = trans_status
            bqsy.char2 = paymentmethod + "|" + payment_channel + "|" + trans_id_merchant
            bqsy.date1 = get_current_date()


            result_message = "0_Operation Success"
            trans_status = bqsy.char1 + " transID == " + bqsy.char2

            bqsy = db_session.query(Bqsy).first()

        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 223
            queasy.number1 = outletno
            queasy.number3 = paymentcode
            queasy.char1 = trans_status
            queasy.char2 = paymentmethod + "|" + payment_channel + "|" + trans_id_merchant
            queasy.char3 = session_parameter
            queasy.date1 = get_current_date()


            result_message = "0_Operation Success"
            trans_status = queasy.char1 + " transID == " + queasy.char2

    return generate_output()