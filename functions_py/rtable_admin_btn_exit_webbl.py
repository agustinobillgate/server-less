#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Tisch, Queasy

t_list_data, T_list = create_model_like(Tisch)

def rtable_admin_btn_exit_webbl(t_list_data:[T_list], case_type:int):

    prepare_cache ([Tisch])

    result_message = ""
    tisch = queasy = None

    t_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_message, tisch, queasy
        nonlocal case_type


        nonlocal t_list

        return {"result_message": result_message}

    def fill_new_tisch():

        nonlocal result_message, tisch, queasy
        nonlocal case_type


        nonlocal t_list


        buffer_copy(t_list, tisch)

        if tisch.roomcharge:
            tisch.normalbeleg = 1

    result_message = ""

    t_list = query(t_list_data, first=True)

    if case_type == 1:
        tisch = Tisch()
        db_session.add(tisch)

        fill_new_tisch()

    elif case_type == 2:

        # tisch = get_cache (Tisch, {"departement": [(eq, t_list.departement)],"tischnr": [(eq, t_list.tischnr)]})
        tisch = db_session.query(Tisch).filter(
                 (Tisch.departement == t_list.departement) &
                 (Tisch.tischnr == t_list.tischnr)).with_for_update().first()

        if tisch:

            # queasy = get_cache (Queasy, {"key": [(eq, 31)],"number1": [(eq, tisch.departement)],"number2": [(eq, tisch.tischnr)],"betriebsnr": [(eq, 0)],"deci3": [(eq, tisch.betriebsnr),(ne, t_list.betriebsnr)]})
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 31) &
                     (Queasy.number1 == tisch.departement) &
                     (Queasy.number2 == tisch.tischnr) &
                     (Queasy.betriebsnr == 0) &
                     (Queasy.deci3 != tisch.betriebsnr) &
                     (Queasy.deci3 != t_list.betriebsnr)).with_for_update().first()
            if queasy:
                pass
                db_session.delete(queasy)
                result_message = "Saved table position deleted - " + to_string(tisch.tischnr, "99") + " "
            pass
            tisch.bezeich = t_list.bezeich
            tisch.normalbeleg = t_list.normalbeleg
            tisch.roomcharge = t_list.roomcharge
            tisch.betriebsnr = t_list.betriebsnr

            if t_list.roomcharge:
                tisch.normalbeleg = 1
            pass
            pass
            result_message = result_message + "Success"

    return generate_output()