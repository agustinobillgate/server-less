#using conversion tools version: 1.0.0.117
#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 26/11/2025, with_for_update, skip, temp-table
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Guestbook

def delete_guestbookbl(gastno:int):
    guestbook = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestbook
        nonlocal gastno

        return {}


    # guestbook = get_cache (Guestbook, {"gastnr": [(eq, gastno)]})
    guestbook = db_session.query(Guestbook).filter(
             (Guestbook.gastnr == gastno)).with_for_update().first()

    if guestbook:
        db_session.delete(guestbook)
        pass

    return generate_output()