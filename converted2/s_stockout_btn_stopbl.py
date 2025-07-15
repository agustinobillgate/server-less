#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def s_stockout_btn_stopbl(rec_id:int):
    l_ophdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_ophdr
        nonlocal rec_id

        return {}


    l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, rec_id)]})

    if l_ophdr:
        pass
        db_session.delete(l_ophdr)
        pass

    return generate_output()