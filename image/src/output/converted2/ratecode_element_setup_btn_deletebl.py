#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

def ratecode_element_setup_btn_deletebl(number1:int, user_init:string):

    prepare_cache ([Bediener, Res_history])

    str_msg = ""
    nr:int = 0
    num1:int = 0
    ratecode:string = ""
    queasy = bediener = res_history = None

    bqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_msg, nr, num1, ratecode, queasy, bediener, res_history
        nonlocal number1, user_init
        nonlocal bqueasy


        nonlocal bqueasy

        return {"str_msg": str_msg}


    queasy = get_cache (Queasy, {"key": [(eq, 287)],"number1": [(eq, number1)]})

    if queasy:
        ratecode = queasy.char1

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy.key == 289) & (Bqueasy.char2 == (ratecode).lower())).first()

        if bqueasy:
            str_msg = "Rate Code Element is currently being used, cannot be deleted"
        else:
            pass
            db_session.delete(queasy)
            pass

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Delete ratecode Element, Code: " + ratecode
                res_history.action = "ratecode Element"


                pass
                pass

    return generate_output()