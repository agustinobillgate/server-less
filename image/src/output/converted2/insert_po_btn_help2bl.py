#using conversion tools version: 1.0.0.111

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


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
    pass
    l_artikel.lief_einheit =  to_decimal("1")
    pass

    return generate_output()