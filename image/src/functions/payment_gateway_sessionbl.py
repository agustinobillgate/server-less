from functions.additional_functions import *
import decimal
from models import Queasy

def payment_gateway_sessionbl(resnr:int, reslinnr:int, trans_id_merchant:str, case_step:int):
    trans_status = ""
    mess_str = ""
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal trans_status, mess_str, queasy


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
        mess_str = "1_Transaction Id Merchant can't be Null"

        return generate_output()

    if (case_step != 2 or case_step != 8):
        mess_str = "3_Wrong Case Step, should be 2 or 8"

        return generate_output()

    if resnr == 0:
        mess_str = "5_resnr can't be Null"

        return generate_output()

    if reslinnr == 0:
        mess_str = "6_reslinnr can't be Null"

        return generate_output()

    if case_step == 2:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 223) &  (Queasy.number1 == resnr) &  (Queasy.number2 == reslinnr)).first()

        if queasy:
            mess_str = "4_Transaction Already Exist!"
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


            mess_str = "0_Operation Success"

            return generate_output()