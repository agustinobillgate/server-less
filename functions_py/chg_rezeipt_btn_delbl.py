#using conversion tools version: 1.0.0.117
#------------------------------------------------
# Rulita, 10-09-2025 
# Recompile
# ticket: 5BE11A
#------------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezlin

def chg_rezeipt_btn_delbl(h_recid:int):
    h_rezlin = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_rezlin
        nonlocal h_recid

        return {}


    h_rezlin = get_cache (H_rezlin, {"_recid": [(eq, h_recid)]})

    if h_rezlin:
        pass
        db_session.delete(h_rezlin)

    return generate_output()