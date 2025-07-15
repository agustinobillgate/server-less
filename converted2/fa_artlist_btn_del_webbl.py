#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Mathis, Fa_artikel, Queasy

def fa_artlist_btn_del_webbl(mathis_nr:int):
    mathis = fa_artikel = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mathis, fa_artikel, queasy
        nonlocal mathis_nr

        return {}


    mathis = get_cache (Mathis, {"nr": [(eq, mathis_nr)]})

    if mathis:
        pass
        db_session.delete(mathis)
        pass

        fa_artikel = get_cache (Fa_artikel, {"nr": [(eq, mathis_nr)]})

        if fa_artikel:
            pass
            db_session.delete(fa_artikel)
            pass

        queasy = get_cache (Queasy, {"key": [(eq, 314)],"number1": [(eq, mathis_nr)]})

        if queasy:
            pass
            db_session.delete(queasy)
            pass

    return generate_output()