#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 04/08/2025
# gitlab: -
# remarks: -
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Guestbud

def guestbud1_btn_delbl(rec_id:int):
    guestbud = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestbud
        nonlocal rec_id

        return {}


    guestbud = get_cache (Guestbud, {"_recid": [(eq, rec_id)]})
    # Rd 4/8/2025
    if guestbud:
        db_session.delete(guestbud)

    return generate_output()