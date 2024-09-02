from functions.additional_functions import *
import decimal
from models import L_artikel

def insert_po_btn_help2bl(s_artnr:int):
    l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_artikel


        return {}


    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    l_artikel = db_session.query(L_artikel).first()
    l_artikel.lief_einheit = 1

    l_artikel = db_session.query(L_artikel).first()

    return generate_output()