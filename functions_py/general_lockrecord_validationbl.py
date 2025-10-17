#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 17/10/
# custom gettimestamp,modified code 
#------------------------------------------

from functions.additional_functions import *
from datetime import datetime, timezone
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Res_line

t_input_list_data, T_input_list = create_model("T_input_list", {"v_mode":int, "curr_room":string, "res_number":int, "reslin_number":int, "user_initial":string, "arrival_date":date, "depart_date":date})

def general_lockrecord_validationbl(t_input_list_data:[T_input_list]):

    prepare_cache ([Htparam, Res_line])

    t_output_data_data = []
    is_overlap:bool = False
    time_stamp_str:string = ""
    vbilldate:date = None
    queasy = htparam = res_line = None

    t_input_list = t_output_data = queasy_359 = None

    t_output_data_data, T_output_data = create_model("T_output_data", {"v_success":bool, "error_message":string})

    Queasy_359 = create_buffer("Queasy_359",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_output_data_data, is_overlap, time_stamp_str, vbilldate, queasy, htparam, res_line
        nonlocal queasy_359


        nonlocal t_input_list, t_output_data, queasy_359
        nonlocal t_output_data_data

        return {"t-output-data": t_output_data_data}

        
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

    t_input_list = query(t_input_list_data, first=True)

    if not t_input_list:
        t_output_data = T_output_data()
        t_output_data_data.append(t_output_data)

        t_output_data.v_success = False
        t_output_data.error_message = "No Data Input List Available"

        return generate_output()
    t_output_data = T_output_data()
    t_output_data_data.append(t_output_data)


    if t_input_list.v_mode == 1:

        queasy_359 = db_session.query(Queasy_359).filter(
                 (Queasy_359.key == 359) & (Queasy_359.number1 == t_input_list.res_number) & (Queasy_359.number2 == t_input_list.reslin_number) & (Queasy_359.number3 == 1)).first()

        if queasy_359:
            db_session.delete(queasy_359)
            pass

        queasy = get_cache (Queasy, {"key": [(eq, 359)],"char1": [(eq, t_input_list.curr_room)],"number1": [(eq, t_input_list.res_number)],"number2": [(eq, t_input_list.reslin_number)],"number3": [(eq, 1)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 359
            queasy.char1 = t_input_list.curr_room
            queasy.char2 = t_input_list.user_initial
            queasy.char3 = get_timestamp_with_ms()
            queasy.number1 = t_input_list.res_number
            queasy.number2 = t_input_list.reslin_number
            queasy.number3 = 1
            queasy.date1 = t_input_list.arrival_date
            queasy.date2 = t_input_list.depart_date


        t_output_data.v_success = True
        t_output_data.error_message = ""

    elif t_input_list.v_mode == 2:

        queasy = get_cache (Queasy, {"key": [(eq, 359)],"number3": [(eq, 1)],"number1": [(eq, t_input_list.res_number)],"number2": [(eq, t_input_list.reslin_number)]})

        if queasy:
            db_session.delete(queasy)
            pass
        t_output_data.v_success = True
        t_output_data.error_message = ""

    elif t_input_list.v_mode == 3:

        res_line_obj_list = {}
        for res_line in db_session.query(Res_line).filter(
                 (Res_line._recid.in_(list(set([t_input_list.res_number for t_input_list in t_input_list_data]))))).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            queasy = get_cache (Queasy, {"key": [(eq, 359)],"number3": [(eq, 1)],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

            if queasy:
                db_session.delete(queasy)
                pass
            t_output_data.v_success = True
            t_output_data.error_message = ""

    return generate_output()