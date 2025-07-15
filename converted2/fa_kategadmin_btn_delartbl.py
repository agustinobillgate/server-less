#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_kateg, Fa_artikel

def fa_kategadmin_btn_delartbl(rec_id:int):
    do_it = True
    fa_kateg = fa_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, fa_kateg, fa_artikel
        nonlocal rec_id

        return {"do_it": do_it}


    fa_kateg = get_cache (Fa_kateg, {"_recid": [(eq, rec_id)]})

    if fa_kateg:

        fa_artikel = get_cache (Fa_artikel, {"katnr": [(eq, fa_kateg.katnr)]})

        if fa_artikel:
            do_it = False
        else:
            pass
            db_session.delete(fa_kateg)
            pass

    return generate_output()