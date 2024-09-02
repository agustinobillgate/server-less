from functions.additional_functions import *
import decimal
from models import L_orderhdr

def mk_po_valchg_releaseflagbl(rec_id:int):
    l_orderhdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr


        return {}


    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == rec_id)).first()

    l_orderhdr = db_session.query(L_orderhdr).first()
    l_orderhdr.gedruckt = get_current_date()

    l_orderhdr = db_session.query(L_orderhdr).first()

    return generate_output()