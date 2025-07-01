#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

book_engine_list_list, Book_engine_list = create_model_like(Queasy)

def bookengine_admin_btn_exitbl(book_engine_list_list:[Book_engine_list], icase:int):

    prepare_cache ([Queasy])

    queasy = None

    book_engine_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal icase


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


    else:

        queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, book_engine_list.number1)]})

        if queasy:
            buffer_copy(book_engine_list, queasy)

    return generate_output()