from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line

def reservation_btn_checkinbl(pvilanguage:int, resno:int, reslinno:int):
    error_number = 0
    msg_str = ""
    ci_date:date = None
    lvcarea:str = "reservation"
    res_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_number, msg_str, ci_date, lvcarea, res_line


        return {"error_number": error_number, "msg_str": msg_str}

    def check_in():

        nonlocal error_number, msg_str, ci_date, lvcarea, res_line


        ci_date = get_output(htpdate(87))

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

        if not res_line:
            msg_str = translateExtended ("Reservation record not yet selected.", lvcarea, "")
            error_number = 1

            return

        if ((res_line.ankunft != ci_date) or (res_line.active_flag != 0)):
            error_number = 2

            return

        if res_line.l_zuordnung[2] == 1:
            msg_str = translateExtended ("Check_in function not for accompanying guest.", lvcarea, "")
            error_number = 3

            return

    check_in()

    return generate_output()