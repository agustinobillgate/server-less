#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 4/8/2025
# if available
# Rd, 27/11/2025, with_for_update added
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


    # queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy._recid == rec_id)).with_for_update().first()
    # Rd 4/8/2025
    # if available
    if queasy:
        db_session.delete(queasy)

    return generate_output()