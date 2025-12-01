#using conversion tools version: 1.0.0.117
#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import L_untergrup, Queasy

l_list_data, L_list = create_model_like(L_untergrup)

def ssubgrp_admin_btn_exitbl(l_list_data:[L_list], case_type:int, fibukonto:string, engart:bool, main_nr:int):

    prepare_cache ([L_untergrup])

    l_untergrup = queasy = None

    l_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_untergrup, queasy
        nonlocal case_type, fibukonto, engart, main_nr


        nonlocal l_list

        return {}

    l_list = query(l_list_data, first=True)

    if not l_list:

        return generate_output()

    if case_type == 1:
        l_untergrup = L_untergrup()
        db_session.add(l_untergrup)

        l_untergrup.zwkum = l_list.zwkum
        l_untergrup.bezeich = l_list.bezeich
        l_untergrup.fibukonto = fibukonto

        if engart :
            l_untergrup.betriebsnr = 1
        else:
            l_untergrup.betriebsnr = 0

        # queasy = get_cache (Queasy, {"key": [(eq, 29)],"number2": [(eq, l_untergrup.zwkum)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 29) &
                 (Queasy.number2 == l_untergrup.zwkum)).with_for_update().first()

        if main_nr > 0:

            if queasy:
                queasy.number1 = main_nr
            else:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 29
                queasy.number1 = main_nr
                queasy.number2 = l_list.zwkum


            pass

        elif queasy:
            db_session.delete(queasy)

    elif case_type == 2:

        # l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_list.zwkum)]})
        l_untergrup = db_session.query(L_untergrup).filter(
                 (L_untergrup.zwkum == l_list.zwkum)).with_for_update().first()
        pass
        l_untergrup.bezeich = l_list.bezeich
        l_untergrup.fibukonto = fibukonto

        if engart:
            l_untergrup.betriebsnr = 1
        else:
            l_untergrup.betriebsnr = 0

        # queasy = get_cache (Queasy, {"key": [(eq, 29)],"number2": [(eq, l_untergrup.zwkum)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 29) &
                 (Queasy.number2 == l_untergrup.zwkum)).with_for_update().first()

        if main_nr > 0:

            if queasy:
                queasy.number1 = main_nr
            else:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 29
                queasy.number1 = main_nr
                queasy.number2 = l_list.zwkum


            pass

        elif queasy:
            db_session.delete(queasy)
        pass

    return generate_output()