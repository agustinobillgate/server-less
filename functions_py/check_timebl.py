#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 16-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================
# Rd, 26/11/2025, with_for_update, skip, temp-table
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

def check_timebl(case_type:int, id_table:int, id_table1:int, name_table:string, init_time2:int, init_date2:date):
    flag_ok = False
    init_time1 = 0
    init_date1 = None
    delta_time:int = 0
    init_time:int = 0
    init_date:date = None
    setting_time:int = 0
    tmp_time:int = 0
    tmp_today:int = 0
    con_day:date = None
    queasy = None

    db_session = local_storage.db_session
    name_table = name_table.strip()

    def generate_output():
        nonlocal flag_ok, init_time1, init_date1, delta_time, init_time, init_date, setting_time, tmp_time, tmp_today, con_day, queasy
        nonlocal case_type, id_table, id_table1, name_table, init_time2, init_date2

        return {"flag_ok": flag_ok, "init_time1": init_time1, "init_date1": init_date1}


    if name_table == None:

        return generate_output()
    setting_time = (3 * 60)
    init_time = get_current_time_in_seconds()
    init_date = get_current_date()
    init_time1 = init_time
    init_date1 = init_date

    if case_type == 1:

        if id_table1 != None:

            queasy = get_cache (Queasy, {"key": [(eq, 9999)],"char1": [(eq, name_table)],"number2": [(eq, id_table)],"number3": [(eq, id_table1)]})
        else:

            queasy = get_cache (Queasy, {"key": [(eq, 9999)],"char1": [(eq, name_table)],"number2": [(eq, id_table)]})

        if queasy:
            con_day = get_current_date()
            tmp_time = get_current_time_in_seconds() - to_int(queasy.number1)
            tmp_today = (con_day - queasy.date1).days
            tmp_today = tmp_today * 24 * 3600


            delta_time = tmp_time + tmp_today

            if delta_time < setting_time:

                return generate_output()
            else:
                pass
                queasy.number1 = init_time
                queasy.date1 = init_date


                pass
                pass
                flag_ok = True
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 9999
            queasy.char1 = name_table
            queasy.number1 = init_time
            queasy.number2 = id_table
            queasy.date1 = init_date

            if id_table1 != None:
                queasy.number3 = id_table1


            flag_ok = True

    elif case_type == 2:

        if id_table1 != None:

            # queasy = get_cache (Queasy, {"key": [(eq, 9999)],"char1": [(eq, name_table)],"number2": [(eq, id_table)],"number3": [(eq, id_table1)]})
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 9999) &
                     (Queasy.char1 == name_table) &
                     (Queasy.number2 == id_table) &
                     (Queasy.number3 == id_table1)).with_for_update().first()
        else:

            # queasy = get_cache (Queasy, {"key": [(eq, 9999)],"char1": [(eq, name_table)],"number2": [(eq, id_table)]})
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 9999) &
                     (Queasy.char1 == name_table) &
                     (Queasy.number2 == id_table)).with_for_update().first()

        if queasy:

            if init_date2 == queasy.date1 and init_time2 == queasy.number1:
                pass
                db_session.delete(queasy)
                pass
                flag_ok = True

    elif case_type == 3:

        if id_table1 != None:

            queasy = get_cache (Queasy, {"key": [(eq, 9999)],"char1": [(eq, name_table)],"number2": [(eq, id_table)],"number3": [(eq, id_table1)]})
        else:

            queasy = get_cache (Queasy, {"key": [(eq, 9999)],"char1": [(eq, name_table)],"number2": [(eq, id_table)]})

        if queasy:

            if init_date2 == queasy.date1 and init_time2 == queasy.number1:
                flag_ok = True

    return generate_output()