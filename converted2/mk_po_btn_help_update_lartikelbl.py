from functions.additional_functions import *
import decimal
from models import L_artikel

def mk_po_btn_help_update_lartikelbl(rec_id:int):
    l_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_artikel
        nonlocal rec_id


        return {}


    l_artikel = db_session.query(L_artikel).filter(
             (L_artikel._recid == rec_id)).first()
    l_artikel.lief_einheit =  to_decimal("1")

    return generate_output()