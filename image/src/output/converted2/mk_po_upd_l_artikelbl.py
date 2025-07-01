#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def mk_po_upd_l_artikelbl(rec_id:int):

    prepare_cache ([L_artikel])

    l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_artikel
        nonlocal rec_id

        return {}


    l_artikel = get_cache (L_artikel, {"_recid": [(eq, rec_id)]})
    pass
    l_artikel.lief_einheit =  to_decimal("1")
    pass

    return generate_output()