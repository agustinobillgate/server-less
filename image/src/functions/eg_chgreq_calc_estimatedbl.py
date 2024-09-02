from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Eg_subtask, Eg_duration

def eg_chgreq_calc_estimatedbl(r_sub_task:str, intime:int, indate:date):
    r_ex_finishdate = None
    r_ex_finishtime = 0
    estfin_str = ""
    adtime:int = 0
    stime:int = 0
    d:date = None
    e:date = None
    f:int = 0
    eg_subtask = eg_duration = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal r_ex_finishdate, r_ex_finishtime, estfin_str, adtime, stime, d, e, f, eg_subtask, eg_duration


        return {"r_ex_finishdate": r_ex_finishdate, "r_ex_finishtime": r_ex_finishtime, "estfin_str": estfin_str}


    eg_subtask = db_session.query(Eg_subtask).filter(
            (func.lower(Eg_subtask.sub_code) == (r_sub_task).lower())).first()

    if eg_subtask:

        eg_duration = db_session.query(Eg_duration).filter(
                (Eg_duration.duration_nr == eg_subtask.dur_nr)).first()

        if eg_duration:

            if eg_duration.hour != 0:
                adtime = eg_duration.hour * 3600

            if eg_duration.minute != 0:
                adtime = adtime + (eg_duration.minute * 60)
            stime = intime + adtime

            if stime < 86399:
                d = indate
                f = stime
            else:
                d = indate
                while (stime > 86399) :
                    d = d + 1
                    stime = stime - 86399
                    f = stime

            if eg_duration.DAY != 0:
                e = d + eg_duration.DAY
            else:
                e = d
            r_ex_finishdate = e
            r_ex_finishtime = f
            estfin_str = replace (to_string(f, "HH:MM") , ":", "")

    return generate_output()