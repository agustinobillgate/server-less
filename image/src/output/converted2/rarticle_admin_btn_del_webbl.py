#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, H_umsatz, Queasy

def rarticle_admin_btn_del_webbl(h_artnr:int, h_dept:int):
    flag = 0
    h_artikel = h_umsatz = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, h_artikel, h_umsatz, queasy
        nonlocal h_artnr, h_dept

        return {"flag": flag}


    h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_artnr)],"departement": [(eq, h_dept)]})

    h_umsatz = get_cache (H_umsatz, {"artnr": [(eq, h_artnr)],"departement": [(eq, h_dept)]})

    if h_umsatz:
        flag = 1
    else:
        flag = 2
        pass
        db_session.delete(h_artikel)

        queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 2)],"number2": [(eq, h_artnr)],"number3": [(eq, h_dept)]})

        if queasy:
            pass
            db_session.delete(queasy)
            pass

    return generate_output()