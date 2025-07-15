#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

def industry_type_config_deletebl(selected_guest:int, user_init:string):

    prepare_cache ([Queasy, Bediener, Res_history])

    temp_list_data = []
    num1:int = 0
    nr:int = 0
    category:string = ""
    queasy = bediener = res_history = None

    temp_list = b_queasy = None

    temp_list_data, Temp_list = create_model("Temp_list", {"number1":int, "number2":int, "char1":string, "number3":int, "category":string})

    B_queasy = create_buffer("B_queasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_list_data, num1, nr, category, queasy, bediener, res_history
        nonlocal selected_guest, user_init
        nonlocal b_queasy


        nonlocal temp_list, b_queasy
        nonlocal temp_list_data

        return {"temp-list": temp_list_data}

    queasy = get_cache (Queasy, {"key": [(eq, 282)],"number3": [(eq, selected_guest)]})

    if queasy:
        num1 = queasy.number1
        pass
        db_session.delete(queasy)
        pass

        b_queasy = get_cache (Queasy, {"key": [(eq, 281)],"number1": [(eq, num1)]})

        if b_queasy:
            category = b_queasy.char1

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Delete Guest from KeyAccount, GuestNo: " + to_string(selected_guest) + " KeyAccount: " + category
            res_history.action = "Key Account"


            pass
            pass

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 282) & (Queasy.number1 == num1)).order_by(Queasy._recid).all():
        nr = nr + 1
        queasy.number2 = nr


    temp_list_data.clear()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 282)).order_by(Queasy._recid).all():

        b_queasy = get_cache (Queasy, {"key": [(eq, 281)],"number1": [(eq, queasy.number1)]})

        if b_queasy:
            temp_list = Temp_list()
            temp_list_data.append(temp_list)

            temp_list.number1 = queasy.number1
            temp_list.number2 = queasy.number2
            temp_list.char1 = queasy.char1
            temp_list.number3 = queasy.number3

            if queasy.number1 == b_queasy.number1:
                temp_list.category = b_queasy.char1

    return generate_output()