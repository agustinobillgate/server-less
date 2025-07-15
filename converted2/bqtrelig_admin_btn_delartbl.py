#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def bqtrelig_admin_btn_delartbl(rec_id:int):
    err = 0
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, queasy
        nonlocal rec_id

        return {"err": err}


    queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})

    if queasy:
        pass
        db_session.delete(queasy)
        pass

    return generate_output()