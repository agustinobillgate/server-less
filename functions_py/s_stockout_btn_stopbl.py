#using conversion tools version: 1.0.0.119

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
    
    l_ophdr = db_session.query(L_ophdr).filter(L_ophdr._recid == rec_id).first()

    if l_ophdr:
        db_session.refresh(l_ophdr, with_for_update=True)
        db_session.delete(l_ophdr)
        db_session.flush()

    return generate_output()