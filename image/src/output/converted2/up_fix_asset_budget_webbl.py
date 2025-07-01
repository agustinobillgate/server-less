#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Bediener, Res_history

def up_fix_asset_budget_webbl(nr_budget:int, desc_budget:string, date_budget:date, amount_budget:Decimal, is_active_budget:bool, user_init:string):

    prepare_cache ([Queasy, Bediener, Res_history])

    err_mark = ""
    rec_id:int = 0
    queasy = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_mark, rec_id, queasy, bediener, res_history
        nonlocal nr_budget, desc_budget, date_budget, amount_budget, is_active_budget, user_init

        return {"err_mark": err_mark}

    def convert_status(statusinp:bool):

        nonlocal err_mark, rec_id, queasy, bediener, res_history
        nonlocal nr_budget, desc_budget, date_budget, amount_budget, is_active_budget, user_init

        if statusinp:
            return "Active"
        else:
            return "Deactive"


    def update_it():

        nonlocal err_mark, rec_id, queasy, bediener, res_history
        nonlocal nr_budget, desc_budget, date_budget, amount_budget, is_active_budget, user_init

        oldstatus:string = ""
        oldstatus = queasy.char1 + ", date: " + to_string(queasy.date1) + ", amount: " + to_string(queasy.deci1) + ", status: " + convert_status (queasy.logi1)

        queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})

        if queasy:
            pass
            queasy.char1 = desc_budget
            queasy.date1 = date_budget
            queasy.deci1 =  to_decimal(amount_budget)
            queasy.logi1 = is_active_budget


            pass
            pass

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Fix Asset Budget"
        res_history.aenderung = "Modify Fix Asset Budget with number " + to_string(nr_budget) +\
                " from " + oldstatus + " to " + desc_budget + ", date: " + to_string(date_budget) +\
                ", amount: " + to_string(amount_budget) + ", status: " + convert_status (is_active_budget)

    queasy = get_cache (Queasy, {"key": [(eq, 324)],"number1": [(eq, nr_budget)]})

    if queasy:
        rec_id = queasy._recid
        update_it()
    else:
        err_mark = "budget-fix-asset-is-not-found"

    return generate_output()