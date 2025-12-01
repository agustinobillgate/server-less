#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def insert_po_btn_help2bl(s_artnr:int):

    prepare_cache ([L_artikel])

    l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_artikel
        nonlocal s_artnr

        return {}


    # l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
    l_artikel = db_session.query(L_artikel).filter(
             (L_artikel.artnr == s_artnr)).with_for_update().first()
    l_artikel.lief_einheit =  to_decimal("1")

    return generate_output()