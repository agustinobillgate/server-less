#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Mathis, Fa_artikel

def fa_artlist_btn_delbl(mathis_nr:int):
    mathis = fa_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mathis, fa_artikel
        nonlocal mathis_nr

        return {}


    mathis = get_cache (Mathis, {"nr": [(eq, mathis_nr)]})

    if mathis:
        pass
        db_session.delete(mathis)
        pass

    fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, mathis.nr)]})

    if fa_artikel:
        pass
        db_session.delete(fa_artikel)
        pass

    return generate_output()