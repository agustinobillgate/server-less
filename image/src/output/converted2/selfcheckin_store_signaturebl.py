#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Archieve, Res_line

def selfcheckin_store_signaturebl(res_no:int, resline_no:int, guest_number:int, sign_data:string):

    prepare_cache ([Res_line])

    mess_result = ""
    sys_date:string = ""
    image_data:string = ""
    bb:bytes = None
    archieve = res_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, sys_date, image_data, bb, archieve, res_line
        nonlocal res_no, resline_no, guest_number, sign_data

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
        mess_result = "2-Reservation Number Can't be Null!"

        return generate_output()

    if resline_no == 0:
        mess_result = "3-Reservation Line Number Can't be Null!"

        return generate_output()

    if guest_number == 0:
        mess_result = "4-Guest Number Can't be Null!"

        return generate_output()

    if sign_data == "":
        mess_result = "5-Signature Data Can't be Null!"

        return generate_output()

    archieve = get_cache (Archieve, {"key": [(eq, "send-sign-rc")],"num1": [(eq, res_no)],"num2": [(eq, resline_no)],"num3": [(eq, guest_number)]})

    if archieve:
        db_session.delete(archieve)

    res_line = get_cache (Res_line, {"resnr": [(eq, res_no)],"reslinnr": [(eq, resline_no)]})

    if res_line:

        if not matches(res_line.zimmer_wunsch,r"*mobile-sign-rc*"):
            res_line.zimmer_wunsch = res_line.zimmer_wunsch + "mobile-sign-rc;"
        pass
        sys_date = to_string(get_month(get_current_date()) , "99") + "/" + to_string(get_day(get_current_date()) , "99") + "/" + to_string(get_year(get_current_date()) , "9999") + ";" + to_string(get_current_time_in_seconds()) + ";"
        bb = base64_decode(sign_data)
        image_data = bb
        archieve = Archieve()
        db_session.add(archieve)

        archieve.key = "send-sign-rc"
        archieve.num1 = res_no
        archieve.num2 = resline_no
        archieve.num3 = guest_number
        archieve.char[0] = ""
        archieve.char[1] = image_data
        archieve.char[3] = ""
        archieve.char[2] = sys_date
        archieve.datum = res_line.ankunft


        pass
        pass
        mess_result = "0-Save Signature Success"
    else:
        mess_result = "1-No REservation found!"

        return generate_output()

    return generate_output()