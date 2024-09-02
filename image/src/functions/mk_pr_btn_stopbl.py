from functions.additional_functions import *
import decimal
from models import L_orderhdr

def mk_pr_btn_stopbl(rec_id:int):
    l_orderhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr


        return {}


    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == rec_id)).first()
    db_session.delete(l_orderhdr)


    return generate_output()