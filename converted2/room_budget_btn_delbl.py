#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Rmbudget

def room_budget_btn_delbl(rec_id:int):
    rmbudget = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmbudget
        nonlocal rec_id

        return {}


    rmbudget = get_cache (Rmbudget, {"_recid": [(eq, rec_id)]})
    pass
    db_session.delete(rmbudget)
    pass

    return generate_output()