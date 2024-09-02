from functions.additional_functions import *
import decimal
from models import L_untergrup, L_artikel, Queasy

def ssubgrp_admin_btn_delbl(l_untergrup_zwkum:int):
    flag = 0
    l_untergrup = l_artikel = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, l_untergrup, l_artikel, queasy


        return {"flag": flag}


    l_untergrup = db_session.query(L_untergrup).filter(
            (L_untergrup.zwkum == l_untergrup_zwkum)).first()

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.zwkum == l_untergrup_zwkum)).first()

    if l_artikel:
        flag = 1
    else:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 29) &  (Queasy.number2 == l_untergrup_zwkum)).first()

        if queasy:
            db_session.delete(queasy)

        l_untergrup = db_session.query(L_untergrup).first()
        db_session.delete(l_untergrup)

    return generate_output()