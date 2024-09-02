from functions.additional_functions import *
import decimal
from models import L_order

def insert_po_return_bestellerbl(rec_id:int, bemerkung:str):
    l_order = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order


        return {}


    l_order = db_session.query(L_order).filter(
            (L_order.artnr == rec_id)).first()
    l_order.besteller = bemerkung

    l_order = db_session.query(L_order).first()

    return generate_output()