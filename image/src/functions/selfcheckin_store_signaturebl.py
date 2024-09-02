from functions.additional_functions import *
import decimal
from sqlalchemy import func
import re
from models import Archieve, Res_line

def selfcheckin_store_signaturebl(res_no:int, resline_no:int, guest_number:int, sign_data:str):
    mess_result = ""
    sys_date:str = ""
    image_data:str = ""
    bb:bytes = None
    archieve = res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, sys_date, image_data, bb, archieve, res_line


        return {"mess_result": mess_result}


    if res_no == None:
        res_no = 0

    if resline_no == None:
        resline_no = 0

    if guest_number == None:
        guest_number = 0

    if sign_data == None:
        sign_data = ""

    if res_no == 0:
        mess_result = "2_Reservation Number Can't be Null!"

        return generate_output()

    if resline_no == 0:
        mess_result = "3_Reservation Line Number Can't be Null!"

        return generate_output()

    if guest_number == 0:
        mess_result = "4_Guest Number Can't be Null!"

        return generate_output()

    if sign_data == "":
        mess_result = "5_Signature Data Can't be Null!"

        return generate_output()

    archieve = db_session.query(Archieve).filter(
            (func.lower(Archieve.key) == "send_sign_rc") &  (Archieve.num1 == res_no) &  (Archieve.num2 == resline_no) &  (Archieve.num3 == guest_number)).first()

    if archieve:
        db_session.delete(archieve)

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == res_no) &  (Res_line.reslinnr == resline_no)).first()

    if res_line:

        if not re.match(".*mobile_sign_rc.*",res_line.zimmer_wunsch):
            res_line.zimmer_wunsch = res_line.zimmer_wunsch + "mobile_sign_rc;"

        res_line = db_session.query(Res_line).first()
        sys_date = to_string(get_month(get_current_date()) , "99") + "/" + to_string(get_day(get_current_date()) , "99") + "/" + to_string(get_year(get_current_date()) , "9999") + ";" + to_string(get_current_time_in_seconds()) + ";"
        bb = base64_decode(sign_data)
        image_data = GET_STRING (bb, 1, GET_SIZE (bb))
        archieve = Archieve()
        db_session.add(archieve)

        archieve.key = "send_sign_rc"
        archieve.num1 = res_no
        archieve.num2 = resline_no
        archieve.num3 = guest_number
        archieve.CHAR[0] = ""
        archieve.CHAR[1] = image_data
        archieve.CHAR[3] = ""
        archieve.CHAR[2] = sys_date
        archieve.datum = res_line.ankunft

        archieve = db_session.query(Archieve).first()

        mess_result = "0_Save Signature Success"
    else:
        mess_result = "1_No REservation found!"

        return generate_output()