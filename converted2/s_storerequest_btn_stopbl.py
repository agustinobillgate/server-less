#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def s_storerequest_btn_stopbl(recid_l_ophdr:int):
    l_ophdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_ophdr
        nonlocal recid_l_ophdr

        return {}


    l_ophdr = get_cache (L_ophdr, {"_recid": [(eq, recid_l_ophdr)]})
    pass
    db_session.delete(l_ophdr)

    return generate_output()