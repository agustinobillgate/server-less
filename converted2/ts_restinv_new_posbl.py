#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Kellner, Hoteldpt

def ts_restinv_new_posbl(pvilanguage:int, curr_waiter:int, new_dept:int, zugriff:bool, exchg_rate:Decimal):

    prepare_cache ([Kellner, Hoteldpt])

    deptname = ""
    b_title = ""
    msg_str = ""
    fl_code = 0
    lvcarea:string = "TS-restinv"
    kellner = hoteldpt = None

    waiter = None

    Waiter = create_buffer("Waiter",Kellner)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal deptname, b_title, msg_str, fl_code, lvcarea, kellner, hoteldpt
        nonlocal pvilanguage, curr_waiter, new_dept, zugriff, exchg_rate
        nonlocal waiter


        nonlocal waiter

        return {"deptname": deptname, "b_title": b_title, "msg_str": msg_str, "fl_code": fl_code}


    waiter = get_cache (Kellner, {"kellner_nr": [(eq, curr_waiter)],"departement": [(eq, new_dept)]})

    if waiter:

        if zugriff:

            kellner = get_cache (Kellner, {"_recid": [(eq, waiter._recid)]})

            hoteldpt = get_cache (Hoteldpt, {"num": [(eq, new_dept)]})
            deptname = hoteldpt.depart
            b_title = hoteldpt.depart + " " + translateExtended ("Bills", lvcarea, "")

            if waehrung:
                b_title = b_title + " / " + translateExtended ("Today's Exchange Rate", lvcarea, "") + " = " + to_string(exchg_rate)
            fl_code = 1

            return generate_output()
    else:
        fl_code = 2
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Waiter-account not defined in the selected department", lvcarea, "")

    return generate_output()