#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener

def bqtcat_admin_btn_delartbl(rec_id:int):
    err = 0
    queasy = bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, queasy, bediener
        nonlocal rec_id

        return {"err": err}


    queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})

    bediener = get_cache (Bediener, {"user_group": [(eq, int (queasy.char1))],"flag": [(eq, 0)]})

    if bediener:
        err = 1
    else:
        pass
        db_session.delete(queasy)
        pass

    return generate_output()