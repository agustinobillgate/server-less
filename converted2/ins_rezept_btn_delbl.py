#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_rezlin

def ins_rezept_btn_delbl(h_recid:int):
    h_rezlin = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_rezlin
        nonlocal h_recid

        return {}


    h_rezlin = get_cache (H_rezlin, {"_recid": [(eq, h_recid)]})
    db_session.delete(h_rezlin)
    pass

    return generate_output()