from functions.additional_functions import *
import decimal
from models import L_untergrup, Queasy

def prepare_ssubgrp_admin_webbl():
    t_l_untergrup_list = []
    l_untergrup = queasy = None

    t_l_untergrup = None

    t_l_untergrup_list, T_l_untergrup = create_model("T_l_untergrup", {"zwkum":int, "bezeich":str, "fibukonto":str, "betriebsnr":int, "main_nr":int, "eng_art":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_untergrup_list, l_untergrup, queasy


        nonlocal t_l_untergrup
        nonlocal t_l_untergrup_list
        return {"t-l-untergrup": t_l_untergrup_list}

    for l_untergrup in db_session.query(L_untergrup).all():
        t_l_untergrup = T_l_untergrup()
        t_l_untergrup_list.append(t_l_untergrup)

        t_l_untergrup.zwkum = l_untergrup.zwkum
        t_l_untergrup.bezeich = l_untergrup.bezeich
        t_l_untergrup.fibukonto = l_untergrup.fibukonto
        t_l_untergrup.betriebsnr = l_untergrup.betriebsnr

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 29) &  (Queasy.number2 == l_untergrup.zwkum)).first()

        if queasy:
            t_l_untergrup.main_nr = queasy.number1
        else:
            t_l_untergrup.main_nr = 0

        if l_untergrup.betriebsnr == 1:
            t_l_untergrup.eng_art = True
        else:
            t_l_untergrup.eng_art = False

    return generate_output()