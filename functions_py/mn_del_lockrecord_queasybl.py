#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from datetime import datetime, timezone
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

    def get_timestamp_with_ms() -> str:
        """
        Returns current timestamp as a string with millisecond precision,
        equivalent to the Progress ABL getTimestampWithMs function.
        """
        # current UTC time
        now = datetime.now(timezone.utc)

        # Epoch (1970-01-01 UTC)
        epoch = datetime(1970, 1, 1, tzinfo=timezone.utc)

        # milliseconds since epoch
        epoch_milliseconds = int((now - epoch).total_seconds() * 1000)

        # reconstruct human-readable datetime from milliseconds
        human_date = datetime.fromtimestamp(epoch_milliseconds / 1000, tz=timezone.utc)

        # format string same as ABL STRING(DATETIME) output: "YYYY-MM-DDTHH:MM:SS.mmm"
        timestamp_str = human_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]  # trim to milliseconds

        return timestamp_str
    
    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        vbilldate = htparam.fdate

    if v_mode == 1:
        timestamp_str = get_timestamp_with_ms()
        if timestamp_str != "" and num_entries(timestamp_str, " ") >= 1:
            v_date = date_mdy(entry(0, timestamp_str, " "))
            v_time_msecond = entry(1, timestamp_str, " ")

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 359) & (Queasy.number1 != 0) & (Queasy.number2 != 0) & (Queasy.number3 == 1)).order_by(Queasy.char3).all():

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