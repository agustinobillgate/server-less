#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Res_line, Archieve

def store_signaturebl(res_no:int, resline_no:int, gast_no:int, ct:string, update_flag:bool, mobile_no:string, email:string):

    prepare_cache ([Guest, Res_line])

    result_flag = 0
    sys_date:string = ""
    image_data:string = ""
    bb:bytes = None
    guest = res_line = archieve = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_flag, sys_date, image_data, bb, guest, res_line, archieve
        nonlocal res_no, resline_no, gast_no, ct, update_flag, mobile_no, email

        return {"result_flag": result_flag}


    if ct == None or ct == "":
        result_flag = 1

        return generate_output()

    guest = get_cache (Guest, {"gastnr": [(eq, gast_no)]})

    if guest:

        if mobile_no != None:
            guest.mobil_telefon = mobile_no
        else:
            guest.mobil_telefon = ""

        if email != None:
            guest.email_adr = email
        else:
            guest.email_adr = ""
    else:
        result_flag = 1

        return generate_output()
    pass

    res_line = get_cache (Res_line, {"resnr": [(eq, res_no)],"reslinnr": [(eq, resline_no)]})

    if res_line:

        if not matches(res_line.zimmer_wunsch,r"*mobile-sign-rc*"):
            res_line.zimmer_wunsch = res_line.zimmer_wunsch + "mobile-sign-rc;"
        pass

        archieve = get_cache (Archieve, {"key": [(eq, "send-sign-rc")],"num1": [(eq, res_no)],"num2": [(eq, resline_no)]})

        if archieve:
            db_session.delete(archieve)

        archieve = get_cache (Archieve, {"key": [(eq, "send-sign-rc")],"num1": [(eq, res_no)],"num2": [(eq, resline_no)],"num3": [(eq, gast_no)]})

        if not archieve:
            sys_date = to_string(get_month(get_current_date()) , "99") + "/" + to_string(get_day(get_current_date()) , "99") + "/" + to_string(get_year(get_current_date()) , "9999") + ";" + to_string(get_current_time_in_seconds()) + ";"
            archieve = Archieve()
            db_session.add(archieve)

            archieve.key = "send-sign-rc"
            archieve.num1 = res_no
            archieve.num2 = resline_no
            archieve.num3 = gast_no
            archieve.char[0] = ""
            archieve.char[1] = ct
            archieve.char[2] = sys_date
            archieve.char[3] = ""
            archieve.char[4] = ""
            archieve.datum = res_line.ankunft


        else:
            sys_date = to_string(get_month(get_current_date()) , "99") + "/" + to_string(get_day(get_current_date()) , "99") + "/" + to_string(get_year(get_current_date()) , "9999") + ";" + to_string(get_current_time_in_seconds()) + ";"
            archieve.char[0] = ""
            archieve.char[1] = ct
            archieve.char[2] = sys_date
            archieve.char[3] = ""
            archieve.char[4] = ""
            archieve.datum = res_line.ankunft


        pass
        pass

    return generate_output()