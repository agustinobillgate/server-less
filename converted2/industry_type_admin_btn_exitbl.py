#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

temp_list_data, Temp_list = create_model_like(Queasy)

def industry_type_admin_btn_exitbl(temp_list_data:[Temp_list], icase:int, user_init:string):

    prepare_cache ([Queasy, Bediener, Res_history])

    category:string = ""
    category2:string = ""
    queasy = bediener = res_history = None

    temp_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal category, category2, queasy, bediener, res_history
        nonlocal icase, user_init


        nonlocal temp_list

        return {}

    temp_list = query(temp_list_data, first=True)

    if icase == 1:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 281
        queasy.number1 = temp_list.number1
        queasy.char1 = temp_list.char1
        category = temp_list.char1

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Add Industry Type Profile, Name: " + category
            res_history.action = "Industry Type Profile"


            pass
            pass
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 281)],"number1": [(eq, temp_list.number1)]})

        if queasy:
            category = queasy.char1
            buffer_copy(temp_list, queasy)
            category2 = temp_list.char1

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Change Industry Type Profile, From: " + category + " To: " + category2
                res_history.action = "Industry Type Profile"


                pass
                pass

    return generate_output()