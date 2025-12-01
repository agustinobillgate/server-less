#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
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


    # queasy = get_cache (Queasy, {"_recid": [(eq, recid_queasy)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy._recid == recid_queasy)).with_for_update().first()

    if queasy:
        pass
        db_session.delete(queasy)

    return generate_output()