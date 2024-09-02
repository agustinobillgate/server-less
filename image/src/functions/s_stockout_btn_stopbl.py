from functions.additional_functions import *
import decimal
from models import L_ophdr

def s_stockout_btn_stopbl(rec_id:int):
    l_ophdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_ophdr


        return {}


    l_ophdr = db_session.query(L_ophdr).filter(
            (L_ophdr._recid == rec_id)).first()

    l_ophdr = db_session.query(L_ophdr).first()
    db_session.delete(l_ophdr)


    return generate_output()