#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_lager

def fa_storadmin_btn_delartbl(rec_id:int):
    fa_lager = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_lager
        nonlocal rec_id

        return {}


    fa_lager = get_cache (Fa_lager, {"_recid": [(eq, rec_id)]})

    if fa_lager:
        pass
        db_session.delete(fa_lager)
        pass

    return generate_output()