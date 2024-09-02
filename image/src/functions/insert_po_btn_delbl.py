from functions.additional_functions import *
import decimal
from models import L_order

def insert_po_btn_delbl(rec_id:int):
    l_order = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order


        return {}


    l_order = db_session.query(L_order).filter(
            (L_order._recid == rec_id)).first()
    db_session.delete(l_order)

    return generate_output()