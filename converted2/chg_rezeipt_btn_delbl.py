#using conversion tools version: 1.0.0.117

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


    # h_rezlin = get_cache (H_rezlin, {"_recid": [(eq, h_recid)]})
    h_rezlin = db_session.query(H_rezlin).filter(
             (H_rezlin._recid == h_recid)).with_for_update().first()

    if h_rezlin:
        pass
        db_session.delete(h_rezlin)

    return generate_output()