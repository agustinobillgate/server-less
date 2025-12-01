#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
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


    # l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_untergrup_zwkum)]})
    l_untergrup = db_session.query(L_untergrup).filter(
             (L_untergrup.zwkum == l_untergrup_zwkum)).with_for_update().first()

    l_artikel = get_cache (L_artikel, {"zwkum": [(eq, l_untergrup_zwkum)]})

    if l_artikel:
        flag = 1
    else:

        # queasy = get_cache (Queasy, {"key": [(eq, 29)],"number2": [(eq, l_untergrup_zwkum)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 29) &
                 (Queasy.number2 == l_untergrup_zwkum)).with_for_update().first()

        if queasy:
            db_session.delete(queasy)
        pass
        db_session.delete(l_untergrup)

    return generate_output()