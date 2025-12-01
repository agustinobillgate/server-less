#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 04/08/2025
# Rd, 28/11/2025, with_for_update added
#-----------------------------------------
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


    # rmbudget = get_cache (Rmbudget, {"_recid": [(eq, rec_id)]})
    rmbudget = db_session.query(Rmbudget).filter(Rmbudget._recid == rec_id).with_for_update().first()
    if rmbudget:
        db_session.delete(rmbudget)
    
    return generate_output()