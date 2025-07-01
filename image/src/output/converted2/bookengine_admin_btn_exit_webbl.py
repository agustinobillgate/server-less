#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

book_engine_list_list, Book_engine_list = create_model_like(Queasy)

def bookengine_admin_btn_exit_webbl(book_engine_list_list:[Book_engine_list], icase:int, user_init:string):

    prepare_cache ([Queasy, Bediener, Res_history])

    queasy = bediener = res_history = None

    book_engine_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy, bediener, res_history
        nonlocal icase, user_init


        nonlocal book_engine_list

        return {}

    book_engine_list = query(book_engine_list_list, first=True)

    if icase == 1:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 159
        queasy.number1 = book_engine_list.number1
        queasy.char1 = book_engine_list.char1
        queasy.number2 = book_engine_list.number2

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Booking Engine Interface"
            res_history.aenderung = "Created New Booking Engine : BE Code=" + to_string(book_engine_list.number1) + "; Name=" + book_engine_list.char1 + "; Gastnr=" + to_string(book_engine_list.number2) + " by " + to_string(bediener.nr) + " - " + bediener.username


    else:

        queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, book_engine_list.number1)]})

        if queasy:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Booking Engine Interface"
                res_history.aenderung = "Modified Booking Engine : from BE Code=" + to_string(queasy.number1) + " to BE Code=" + to_string(book_engine_list.number1) + "; From Name=" + queasy.char1 + " to Name=" + book_engine_list.char1 + " from Gastnr=" + to_string(queasy.number2) + " To Gastnr=" + to_string(book_engine_list.number2) + " by " + to_string(bediener.nr) + " - " + bediener.username


            buffer_copy(book_engine_list, queasy)

    return generate_output()