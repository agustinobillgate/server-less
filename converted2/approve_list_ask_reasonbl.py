#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def approve_list_ask_reasonbl(pvilanguage:int, trecid:int, user_init:string, reason_str:string, curr_select:string):

    prepare_cache ([Queasy])

    msg_str = ""
    lvcarea:string = "approve-list"
    queasy = None

    qbuff = None

    Qbuff = create_buffer("Qbuff",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, queasy
        nonlocal pvilanguage, trecid, user_init, reason_str, curr_select
        nonlocal qbuff


        nonlocal qbuff

        return {"msg_str": msg_str}


    queasy = get_cache (Queasy, {"_recid": [(eq, trecid)]})

    if queasy:
        qbuff = Queasy()
        db_session.add(qbuff)

        buffer_copy(queasy, qbuff)
        qbuff.logi1 = True
        qbuff.betriebsnr = 1
        qbuff.number2 = to_int(queasy._recid)
        qbuff.char2 = qbuff.char2 + ";" + user_init +\
                to_string(get_month(get_current_date()) , "99") + "/" + to_string(get_day(get_current_date()) , "99") + "/" +\
                to_string((get_year(get_current_date()) - 2000) , "99") + ";" + to_string(get_current_time_in_seconds(), "HH:MM:SS")
        qbuff.char3 = reason_str

        if curr_select.lower()  == ("approve").lower() :
            qbuff.logi2 = True
        else:
            qbuff.logi2 = False
        pass
        pass
        pass
        db_session.delete(queasy)
        pass
    else:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("The request has been cancelled by user.", lvcarea, "") + chr_unicode(10) + translateExtended ("Update no longer possible.", lvcarea, "")

    return generate_output()