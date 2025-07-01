#using conversion tools version: 1.0.0.111

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
    pass
    db_session.delete(guestbud)

    return generate_output()