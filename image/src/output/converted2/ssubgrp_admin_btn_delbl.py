#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_untergrup, L_artikel, Queasy

def ssubgrp_admin_btn_delbl(l_untergrup_zwkum:int):
    flag = 0
    l_untergrup = l_artikel = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, l_untergrup, l_artikel, queasy
        nonlocal l_untergrup_zwkum

        return {"flag": flag}


    l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_untergrup_zwkum)]})

    l_artikel = get_cache (L_artikel, {"zwkum": [(eq, l_untergrup_zwkum)]})

    if l_artikel:
        flag = 1
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 29)],"number2": [(eq, l_untergrup_zwkum)]})

        if queasy:
            db_session.delete(queasy)
        pass
        db_session.delete(l_untergrup)

    return generate_output()