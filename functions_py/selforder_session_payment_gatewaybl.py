#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def selforder_session_payment_gatewaybl(session_parameter:string, trans_id_merchant:string, outletno:int, payment_type:int, payment_channel:string):

    prepare_cache ([Queasy])

    trans_status = ""
    result_message = ""
    paymentmethod:string = ""
    paymentcode:int = 0
    queasy = None

    bqsy = None

    Bqsy = create_buffer("Bqsy",Queasy)

    db_session = local_storage.db_session
    session_parameter = session_parameter.strip()
    payment_channel = payment_channel.strip()
    trans_id_merchant = trans_id_merchant.strip()

    def generate_output():
        nonlocal trans_status, result_message, paymentmethod, paymentcode, queasy
        nonlocal session_parameter, trans_id_merchant, outletno, payment_type, payment_channel
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
        result_message = "1-Transaction Id Merchant can't be Null"

        return generate_output()

    if payment_type == 1:
        paymentmethod = "MIDtrans"
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
        result_message = "2-Wrong Case Type should be 1=MIDtrans, 2=QRIS, 3=DOKU, 4=XENDIT"

        return generate_output()

    if session_parameter == "":
        result_message = "3-sessionParameter can't be Null"

        return generate_output()

    if outletno == 0:
        result_message = "4-outletno can't be set to 0"

        return generate_output()

    if payment_channel == "":
        result_message = "5-paymentChannel can't be Null"

        return generate_output()
    trans_status = "PENDING"

    # queasy = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, outletno)],"char3": [(eq, session_parameter)]})
    queasy = db_session.query(Queasy).filter(
        (Queasy.key == 223) & (Queasy.number1 == outletno) & (Queasy.char3 == session_parameter)).with_for_update().first()

    if queasy:
        pass
        queasy.char1 = trans_status
        queasy.char2 = paymentmethod + "|" + payment_channel + "|" + trans_id_merchant
        queasy.date1 = get_current_date()


        result_message = "0-Operation Success"
        trans_status = queasy.char1 + " transID=" + queasy.char2
        pass
        pass
    else:

        # bqsy = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, outletno)],"betriebsnr": [(eq, to_int(session_parameter))]})
        bqsy = db_session.query(Queasy).filter(
            (Queasy.key == 223) & (Queasy.number1 == outletno) & (Queasy.betriebsnr == to_int(session_parameter))).with_for_update().first()

        if bqsy:
            pass
            bqsy.char1 = trans_status
            bqsy.char2 = paymentmethod + "|" + payment_channel + "|" + trans_id_merchant
            bqsy.date1 = get_current_date()


            result_message = "0-Operation Success"
            trans_status = bqsy.char1 + " transID=" + bqsy.char2
            pass
            pass
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


            result_message = "0-Operation Success"
            trans_status = queasy.char1 + " transID=" + queasy.char2

    return generate_output()