#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser, Bediener, Res_history, Bk_func

def ba_plan_btn_timebl(resnr:int, reslinnr:int, user_init:string, chg_date:date, begin_time:string, ending_time:string, begin_i:int, ending_i:int):

    prepare_cache ([Bk_reser, Bediener, Res_history, Bk_func])

    week_list:List[string] = ["Sunday ", "Monday ", "Tuesday ", "Wednesday", "Thursday ", "Friday ", "Saturday "]
    bk_reser = bediener = res_history = bk_func = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal week_list, bk_reser, bediener, res_history, bk_func
        nonlocal resnr, reslinnr, user_init, chg_date, begin_time, ending_time, begin_i, ending_i

        return {}


    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)],"veran_resnr": [(eq, reslinnr)]})

    if bk_reser:

        if bk_reser.von_zeit.lower()  != (begin_time).lower()  or bk_reser.bis_zeit.lower()  != (ending_time).lower() :

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Time Changes from " +\
                    to_string(bk_reser.von_zeit, "99:99") + " - " + to_string(bk_reser.bis_zeit, "99:99") + " To " +\
                    to_string(begin_time, "99:99") + " - " + to_string(ending_time, "99:99")
            res_history.action = "Banquet"


            pass
            pass

        if bk_reser.datum != chg_date:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Date Changes from " +\
                    to_string(bk_reser.datum) + " To " + to_string(chg_date)
            res_history.action = "Banquet"


            pass
            pass
        pass
        bk_reser.von_zeit = begin_time
        bk_reser.von_i = begin_i
        bk_reser.bis_zeit = ending_time
        bk_reser.bis_i = ending_i
        bk_reser.datum = chg_date
        bk_reser.bis_datum = chg_date
        pass

        bk_func = get_cache (Bk_func, {"veran_nr": [(eq, bk_reser.veran_nr)],"veran_seite": [(eq, bk_reser.veran_seite)]})

        if bk_func:
            pass
            bk_func.datum = chg_date
            bk_func.bis_datum = chg_date
            bk_func.uhrzeit = to_string(bk_reser.von_zeit, "99:99") + " - " + to_string(bk_reser.bis_zeit, "99:99")
            bk_func.wochentag = week_list[get_weekday(bk_reser.datum) - 1]
            bk_func.uhrzeiten[0] = to_string(bk_reser.von_zeit, "99:99") + " - " + to_string(bk_reser.bis_zeit, "99:99")
            pass
        pass

    return generate_output()