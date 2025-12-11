#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 10-12-2025
# - Added with_for_update before delete query
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy

def mn_del_lockrecord_queasybl(v_mode:int):

    prepare_cache ([Htparam])

    i = 0
    timestamp_str:string = ""
    timestamp_now:string = ""
    v_time_msecond:string = ""
    q_time_msecond:string = ""
    v_date:date = None
    q_v_date:date = None
    vbilldate:date = None
    htparam = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, timestamp_str, timestamp_now, v_time_msecond, q_time_msecond, v_date, q_v_date, vbilldate, htparam, queasy
        nonlocal v_mode

        return {"i": i}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        vbilldate = htparam.fdate

    if v_mode == 1:

        if timestamp_str != "" and num_entries(timestamp_str, " ") >= 1:
            v_date = date_mdy(entry(0, timestamp_str, " "))
            v_time_msecond = entry(1, timestamp_str, " ")

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 359) & (Queasy.number1 != 0) & (Queasy.number2 != 0) & (Queasy.number3 == 1)).order_by(Queasy.char3).with_for_update().all():

            if queasy.char3 != "" and num_entries(queasy.char3, " ") >= 1:
                q_v_date = date_mdy(entry(0, queasy.char3, " "))
                q_time_msecond = entry(1, queasy.char3, " ")

                if (v_date - q_v_date) == 1:

                    if v_time_msecond.lower()  >= (q_time_msecond).lower() :
                        db_session.delete(queasy)
                        pass
                        i = i + 1

                elif (v_date - q_v_date) >= 2:
                    db_session.delete(queasy)
                    pass
                    i = i + 1
        pass

    return generate_output()