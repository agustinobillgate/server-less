#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def basetup_email_btn_delartbl(recid_queasy:int):
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal recid_queasy

        return {}


    queasy = get_cache (Queasy, {"_recid": [(eq, recid_queasy)]})
    db_session.delete(queasy)
    pass

    return generate_output()