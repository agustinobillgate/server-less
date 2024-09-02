from functions.additional_functions import *
import decimal
from models import L_untergrup, Queasy

def ssubgrp_admin_btn_exitbl(l_list:[L_list], case_type:int, fibukonto:str, engart:bool, main_nr:int):
    l_untergrup = queasy = None

    l_list = None

    l_list_list, L_list = create_model_like(L_untergrup)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_untergrup, queasy


        nonlocal l_list
        nonlocal l_list_list
        return {}

    l_list = query(l_list_list, first=True)

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

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 29) &  (Queasy.number2 == l_untergrup.zwkum)).first()

        if main_nr > 0:

            if queasy:
                queasy.number1 = main_nr
            else:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 29
                queasy.number1 = main_nr
                queasy.number2 = l_list.zwkum

            queasy = db_session.query(Queasy).first()

        elif queasy:
            db_session.delete(queasy)

    elif case_type == 2:

        l_untergrup = db_session.query(L_untergrup).filter(
                (L_untergrup.zwkum == l_list.zwkum)).first()

        l_untergrup = db_session.query(L_untergrup).first()
        l_untergrup.bezeich = l_list.bezeich
        l_untergrup.fibukonto = fibukonto

        if engart:
            l_untergrup.betriebsnr = 1
        else:
            l_untergrup.betriebsnr = 0

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 29) &  (Queasy.number2 == l_untergrup.zwkum)).first()

        if main_nr > 0:

            if queasy:
                queasy.number1 = main_nr
            else:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 29
                queasy.number1 = main_nr
                queasy.number2 = l_list.zwkum

            queasy = db_session.query(Queasy).first()

        elif queasy:
            db_session.delete(queasy)

        l_untergrup = db_session.query(L_untergrup).first()

    return generate_output()