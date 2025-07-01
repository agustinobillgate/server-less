#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def bqtbeo_admin_btn_delartbl(recid_queasy:int):
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal recid_queasy

        return {}


    queasy = get_cache (Queasy, {"_recid": [(eq, recid_queasy)]})

    if queasy:
        pass
        db_session.delete(queasy)

    return generate_output()