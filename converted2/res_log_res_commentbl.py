#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_history

def res_log_res_commentbl(his_recid:int):

    prepare_cache ([Res_history])

    res_com = ""
    res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_com, res_history
        nonlocal his_recid

        return {"res_com": res_com}


    res_history = get_cache (Res_history, {"_recid": [(eq, his_recid)]})

    if res_history:
        res_com = res_history.aenderung

    return generate_output()