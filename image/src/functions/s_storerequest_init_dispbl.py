from functions.additional_functions import *
import decimal
from models import L_ophdr

def s_storerequest_init_dispbl():
    recid_l_ophdr = 0
    l_ophdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal recid_l_ophdr, l_ophdr


        return {"recid_l_ophdr": recid_l_ophdr}

    l_ophdr = L_ophdr()
    db_session.add(l_ophdr)


    l_ophdr = db_session.query(L_ophdr).first()

    recid_l_ophdr = l_ophdr._recid

    return generate_output()