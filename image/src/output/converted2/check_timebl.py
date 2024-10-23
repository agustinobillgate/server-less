from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy

def check_timebl(case_type:int, id_table:int, id_table1:int, name_table:str, init_time2:int, init_date2:date):
    flag_ok = False
    init_time1 = 0
    init_date1 = None
    delta_time:int = 0
    init_time:int = 0
    init_date:date = None
    setting_time:int = 0
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag_ok, init_time1, init_date1, delta_time, init_time, init_date, setting_time, queasy
        nonlocal case_type, id_table, id_table1, name_table, init_time2, init_date2


        return {"flag_ok": flag_ok, "init_time1": init_time1, "init_date1": init_date1}

    setting_time = (3 * 60)
    init_time = get_current_time_in_seconds()
    init_date = get_current_date()
    init_time1 = init_time
    init_date1 = init_date

    if case_type == 1:

        if id_table1 != None:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 9999) & (func.lower(Queasy.char1) == (name_table).lower()) & (Queasy.number2 == id_table) & (Queasy.number3 == id_table1)).first()
        else:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 9999) & (func.lower(Queasy.char1) == (name_table).lower()) & (Queasy.number2 == id_table)).first()

        if queasy:
            delta_time = (get_current_time_in_seconds() - to_int(queasy.number1)) + (get_current_date() - queasy.date1) * 24 * 3600

            if delta_time < setting_time:

                return generate_output()
            else:
                queasy.number1 = init_time
                queasy.date1 = init_date


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

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 9999) & (func.lower(Queasy.char1) == (name_table).lower()) & (Queasy.number2 == id_table) & (Queasy.number3 == id_table1)).first()
        else:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 9999) & (func.lower(Queasy.char1) == (name_table).lower()) & (Queasy.number2 == id_table)).first()

        if queasy:

            if init_date2 == queasy.date1 and init_time2 == queasy.number1:
                db_session.delete(queasy)
                pass
                flag_ok = True

    elif case_type == 3:

        if id_table1 != None:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 9999) & (func.lower(Queasy.char1) == (name_table).lower()) & (Queasy.number2 == id_table) & (Queasy.number3 == id_table1)).first()
        else:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 9999) & (func.lower(Queasy.char1) == (name_table).lower()) & (Queasy.number2 == id_table)).first()

        if queasy:

            if init_date2 == queasy.date1 and init_time2 == queasy.number1:
                flag_ok = True

    return generate_output()