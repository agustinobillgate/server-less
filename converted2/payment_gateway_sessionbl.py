#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def payment_gateway_sessionbl(resnr:int, reslinnr:int, trans_id_merchant:string, case_step:int):

    prepare_cache ([Queasy])

    trans_status = ""
    mess_str = ""
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal trans_status, mess_str, queasy
        nonlocal resnr, reslinnr, trans_id_merchant, case_step

        return {"trans_status": trans_status, "mess_str": mess_str}


    if trans_id_merchant == None:
        trans_id_merchant = ""

    if case_step == None:
        case_step = 0

    if resnr == None:
        resnr = 0

    if reslinnr == None:
        reslinnr = 0

    if trans_id_merchant == "":
        mess_str = "1-Transaction Id Merchant can't be Null"

        return generate_output()

    if (case_step != 2 or case_step != 8):
        mess_str = "3-Wrong Case Step, should be 2 or 8"

        return generate_output()

    if resnr == 0:
        mess_str = "5-resnr can't be Null"

        return generate_output()

    if reslinnr == 0:
        mess_str = "6-reslinnr can't be Null"

        return generate_output()

    if case_step == 2:

        queasy = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, resnr)],"number2": [(eq, reslinnr)]})

        if queasy:
            mess_str = "4-Transaction Already Exist!"
            trans_status = queasy.char1

            return generate_output()
        else:
            trans_status = "PENDING"
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 223
            queasy.number1 = resnr
            queasy.number2 = reslinnr
            queasy.number3 = 1
            queasy.char1 = trans_status
            queasy.char2 = trans_id_merchant
            queasy.char3 = ""


            mess_str = "0-Operation Success"

            return generate_output()

    return generate_output()