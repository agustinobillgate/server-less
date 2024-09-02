from functions.additional_functions import *
import decimal
from models import Kellner, Hoteldpt

def ts_restinv_new_posbl(pvilanguage:int, curr_waiter:int, new_dept:int, zugriff:bool, exchg_rate:decimal):
    deptname = ""
    b_title = ""
    msg_str = ""
    fl_code = 0
    lvcarea:str = "TS_restinv"
    kellner = hoteldpt = None

    waiter = None

    Waiter = Kellner

    db_session = local_storage.db_session

    def generate_output():
        nonlocal deptname, b_title, msg_str, fl_code, lvcarea, kellner, hoteldpt
        nonlocal waiter


        nonlocal waiter
        return {"deptname": deptname, "b_title": b_title, "msg_str": msg_str, "fl_code": fl_code}


    waiter = db_session.query(Waiter).filter(
            (Waiter.kellner_nr == curr_waiter) &  (Waiter.departement == new_dept)).first()

    if waiter:

        if zugriff:

            kellner = db_session.query(Kellner).filter(
                    (Kellner._recid == waiter._recid)).first()

            hoteldpt = db_session.query(Hoteldpt).filter(
                    (Hoteldpt.num == new_dept)).first()
            deptname = hoteldpt.depart
            b_title = hoteldpt.depart + " " + translateExtended ("Bills", lvcarea, "")

            if waehrung:
                b_title = b_title + " / " + translateExtended ("Today's Exchange Rate", lvcarea, "") + "  ==  " + to_string(exchg_rate)
            fl_code = 1

            return generate_output()
    else:
        fl_code = 2
        msg_str = msg_str + chr(2) + translateExtended ("Waiter_account not defined in the selected department", lvcarea, "")

    return generate_output()