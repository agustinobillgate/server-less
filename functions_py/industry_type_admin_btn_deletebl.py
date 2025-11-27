#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

def industry_type_admin_btn_deletebl(number1:int, user_init:string):

    prepare_cache ([Bediener, Res_history])

    str_msg = ""
    category:string = ""
    num1:int = 0
    nr:int = 0
    queasy = bediener = res_history = None

    q212 = None

    Q212 = create_buffer("Q212",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_msg, category, num1, nr, queasy, bediener, res_history
        nonlocal number1, user_init
        nonlocal q212


        nonlocal q212

        return {"str_msg": str_msg}


    # queasy = get_cache (Queasy, {"key": [(eq, 281)],"number1": [(eq, number1)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 281) &
             (Queasy.number1 == number1)).with_for_update().first()

    if queasy:
        pass

        q212 = db_session.query(Q212).filter(
                 (Q212.key == 282) & (Q212.number1 == queasy.number1)).first()

        if q212:
            str_msg = "Member entries exist, deleting Industry Type Profile not possible"
        else:
            str_msg = ""
            category = queasy.char1
            db_session.delete(queasy)
            pass

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Delete KeyAccount, Name: " + category
                res_history.action = "Key Account"


                pass
                pass

    return generate_output()