#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

def del_fix_asset_budget_webbl(nr_budget:int, user_init:string):

    prepare_cache ([Bediener, Res_history])

    err_mark = ""
    rec_id:int = 0
    queasy = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_mark, rec_id, queasy, bediener, res_history
        nonlocal nr_budget, user_init

        return {"err_mark": err_mark}

    def convert_status(statusinp:bool):

        nonlocal err_mark, rec_id, queasy, bediener, res_history
        nonlocal nr_budget, user_init

        if statusinp:
            return "Active"
        else:
            return "Deactive"


    def delete_it():

        nonlocal err_mark, rec_id, queasy, bediener, res_history
        nonlocal nr_budget, user_init

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Fix Asset Budget"
        res_history.aenderung = "Delete Fix Asset Budget with number " + to_string(nr_budget) +\
                " as " + queasy.char1 + ", date: " + to_string(queasy.date1) +\
                ", amount: " + to_string(queasy.logi1) + ", status: " + convert_status (queasy.logi1)

        # queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy._recid == rec_id)).with_for_update().first()

        if queasy:
            db_session.delete(queasy)
        db_session.refresh(queasy,with_for_update=True)

    queasy = get_cache (Queasy, {"key": [(eq, 324)],"number1": [(eq, nr_budget)]})

    if queasy:
        rec_id = queasy._recid
        delete_it()
    else:
        err_mark = "budget-fix-asset-is-not-found"

    return generate_output()
