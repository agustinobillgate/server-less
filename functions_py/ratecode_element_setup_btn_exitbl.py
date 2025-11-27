#using conversion tools version: 1.0.0.117
#-------------------------------------------
# Rd, 27/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

temp_list_data, Temp_list = create_model_like(Queasy)

def ratecode_element_setup_btn_exitbl(temp_list_data:[Temp_list], icase:int, user_init:string):

    prepare_cache ([Queasy, Bediener, Res_history])

    ratecode:string = ""
    ratecode2:string = ""
    queasy = bediener = res_history = None

    temp_list = bqueasy = pqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ratecode, ratecode2, queasy, bediener, res_history
        nonlocal icase, user_init
        nonlocal bqueasy, pqueasy


        nonlocal temp_list, bqueasy, pqueasy

        return {}

    temp_list = query(temp_list_data, first=True)

    if icase == 1:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 287
        queasy.number1 = temp_list.number1
        queasy.char1 = temp_list.char1
        ratecode = temp_list.char1

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Add ratecode Element, Code: " + ratecode
            res_history.action = "ratecode Element"


            pass
            pass
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 287)],"number1": [(eq, temp_list.number1)]})

        if queasy:
            ratecode = queasy.char1
            ratecode2 = temp_list.char1
            buffer_copy(temp_list, queasy)

            for bqueasy in db_session.query(Bqueasy).filter(
                     (Bqueasy.key == 289) & (Bqueasy.char2 == (ratecode).lower())).order_by(Bqueasy._recid).all():

                # pqueasy = get_cache (Queasy, {"_recid": [(eq, bqueasy._recid)]})
                pqueasy = db_session.query(Pqueasy).filter(Pqueasy._recid == bqueasy._recid).with_for_update().first()
                pqueasy.char2 = ratecode2


                pass
                pass

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Change ratecode Element, From: " + ratecode + " To: " + ratecode2
                res_history.action = "ratecode Element"


                pass
                pass

    return generate_output()