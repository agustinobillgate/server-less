#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
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


    # fa_lager = get_cache (Fa_lager, {"_recid": [(eq, rec_id)]})
    fa_lager = db_session.query(Fa_lager).filter(Fa_lager._recid == rec_id).with_for_update().first()

    if fa_lager:
        pass
        db_session.delete(fa_lager)
        pass

    return generate_output()