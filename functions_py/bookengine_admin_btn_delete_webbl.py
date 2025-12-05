#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
# from sqlalchemy.orm.attributes import flag_modified
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

def bookengine_admin_btn_delete_webbl(number1:int, user_init:string):

    prepare_cache ([Bediener, Res_history])

    queasy = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy, bediener, res_history
        nonlocal number1, user_init

        return {}


    # queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, number1)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 159) &
             (Queasy.number1 == number1)).with_for_update().first()

    if queasy:

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Booking Engine Interface"
            res_history.aenderung = "Deleted Booking Engine : BE Code=" + to_string(queasy.number1) + "; Name=" + queasy.char1 + "; Gastnr=" + to_string(queasy.number2) + " by " + to_string(bediener.nr) + " - " + bediener.username


        pass
        db_session.delete(queasy)
        pass

    return generate_output()