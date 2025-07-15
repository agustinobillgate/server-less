#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def rest_canceladmin_btn_delbl(rec_id:int):
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal rec_id

        return {}


    queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
    pass
    db_session.delete(queasy)
    pass

    return generate_output()