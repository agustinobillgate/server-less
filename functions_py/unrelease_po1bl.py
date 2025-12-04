#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr

def unrelease_po1bl(docu_nr:string):

    prepare_cache ([L_orderhdr])

    l_orderhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr
        nonlocal docu_nr

        return {}

    l_orderhdr = db_session.query(L_orderhdr).filter(L_orderhdr.docu_nr == docu_nr).with_for_update().first()
    
    db_session.refresh(l_orderhdr, with_for_update=True)
    l_orderhdr.gedruckt = None
    db_session.flush()

    return generate_output()