#using conversion tools version: 1.0.0.119
#------------------------------------------
# Rd, 26/11/2025, with_for_update, skip, temp-table
#------------------------------------------

# ==============================================
# Rulita, 04/12/25
# Fixing error datetime.strptime argument format
# Fixing error added function add_interval_local
# ==============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date, timezone
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

    def gettimestampwithms():

        nonlocal t_output_data_data, is_overlap, time_stamp_str, vbilldate, queasy, htparam, res_line
        nonlocal queasy_359


        nonlocal t_input_list, t_output_data, queasy_359
        nonlocal t_output_data_data

        vdatetime:string = ""
        dtz1:datetime = None
        dtz2:datetime = None
        dtz1_str:string = ""
        epoch_millisecond:int = 0
        human_date:datetime = None
        dtz1 = get_current_datetime()
        # Rulita, 04/12/25
        # Fixing error datetime.strptime argument format
        # dtz2 = "1970_01_01T00:00:00.000"
        # dtz2 = datetime.strptime("1970-01-01T00:00:00.000", "%Y-%m-%dT%H:%M:%S.%f")
        dtz2 = datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc)
        epoch_millisecond = get_interval(dtz1, dtz2, "milliseconds")
        human_date = add_interval_local(dtz2, epoch_millisecond, "milliseconds")
        time_stamp_str = to_string(human_date)
        return time_stamp_str
    
    # Rulita, 04/12/25
    # Fixing error added function add_interval_local
    def add_interval_local(start_date, interval_value, interval_unit):
        interval_unit = interval_unit.rstrip("s")
        interval_unit += "s"
        if interval_unit in ['days', 'weeks', 'hours', 'minutes', 'seconds']:
            kwargs = {interval_unit: interval_value}
            return start_date + timedelta(**kwargs)
        elif interval_unit == 'months':
            return start_date + relativedelta(months=interval_value)
        elif interval_unit == 'years':
            return start_date + relativedelta(years=interval_value)
        elif interval_unit == "milliseconds": 
            return start_date + timedelta(milliseconds=interval_value)
        else:
            raise ValueError("Unsupported interval unit")

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

        # queasy = get_cache (Queasy, {"key": [(eq, 359)],"char1": [(eq, t_input_list.curr_room)],"number1": [(eq, t_input_list.res_number)],"number2": [(eq, t_input_list.reslin_number)],"number3": [(eq, 1)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 359) & (Queasy.char1 == t_input_list.curr_room) & (Queasy.number1 == t_input_list.res_number) & (Queasy.number2 == t_input_list.reslin_number) & (Queasy.number3 == 1)).with_for_update().first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 359
            queasy.char1 = t_input_list.curr_room
            queasy.char2 = t_input_list.user_initial
            queasy.char3 = gettimestampwithms()
            queasy.number1 = t_input_list.res_number
            queasy.number2 = t_input_list.reslin_number
            queasy.number3 = 1
            queasy.date1 = t_input_list.arrival_date
            queasy.date2 = t_input_list.depart_date


        t_output_data.v_success = True
        t_output_data.error_message = ""

    elif t_input_list.v_mode == 2:

        # queasy = get_cache (Queasy, {"key": [(eq, 359)],"number3": [(eq, 1)],"number1": [(eq, t_input_list.res_number)],"number2": [(eq, t_input_list.reslin_number)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 359) & (Queasy.number3 == 1) & (Queasy.number1 == t_input_list.res_number) & (Queasy.number2 == t_input_list.reslin_number)).with_for_update().first()

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

            # queasy = get_cache (Queasy, {"key": [(eq, 359)],"number3": [(eq, 1)],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 359) & (Queasy.number3 == 1) & (Queasy.number1 == res_line.resnr) & (Queasy.number2 == res_line.reslinnr)).with_for_update().first()

            if queasy:
                db_session.delete(queasy)
                pass
            t_output_data.v_success = True
            t_output_data.error_message = ""

    return generate_output()