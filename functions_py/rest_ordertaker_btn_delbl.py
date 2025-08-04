#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 4/8/2025
# if available
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def rest_ordertaker_btn_delbl(rec_id:int):
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal rec_id

        return {}


    queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
    # Rd 4/8/2025
    # if available
    if queasy:
        db_session.delete(queasy)

    return generate_output()