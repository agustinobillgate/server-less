#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def s_storerequest_init_dispbl():

    prepare_cache ([L_ophdr])

    recid_l_ophdr = 0
    l_ophdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal recid_l_ophdr, l_ophdr

        return {"recid_l_ophdr": recid_l_ophdr}

    l_ophdr = L_ophdr()
    db_session.add(l_ophdr)

    pass
    recid_l_ophdr = l_ophdr._recid

    return generate_output()