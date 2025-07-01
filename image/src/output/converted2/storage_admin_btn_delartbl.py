#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lager, L_bestand

def storage_admin_btn_delartbl(lager_nr:int):
    err_code = 0
    l_lager = l_bestand = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, l_lager, l_bestand
        nonlocal lager_nr

        return {"err_code": err_code}


    l_lager = get_cache (L_lager, {"lager_nr": [(eq, lager_nr)]})

    l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, l_lager.lager_nr)]})

    if l_bestand:
        err_code = 1
    else:
        pass
        db_session.delete(l_lager)

    return generate_output()