#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Res_history

def delete_master_planbl(resnr:int, user_init:string):

    prepare_cache ([Bediener, Res_history])

    successflag = False
    blockid:string = ""
    bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, blockid, bediener, res_history
        nonlocal resnr, user_init

        return {"successflag": successflag}


    bk_master = db_session.query(Bk_master).filter(
             (Bk_master.resnr == resnr)).first()

    if bk_master:
        blockid = bk_master.block_id
        bk_master.cancel_flag[0] = True


        pass
        successflag = True
    else:
        successflag = False

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Banquet"
        res_history.aenderung = "Delete Master Plan With Block ID " + blockid

    return generate_output()