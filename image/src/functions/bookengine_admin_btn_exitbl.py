from functions.additional_functions import *
import decimal
from models import Queasy

def bookengine_admin_btn_exitbl(book_engine_list:[Book_engine_list], icase:int):
    queasy = None

    book_engine_list = None

    book_engine_list_list, Book_engine_list = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        nonlocal book_engine_list
        nonlocal book_engine_list_list
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

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 159) &  (Queasy.number1 == book_engine_list.number1)).first()

        if queasy:
            buffer_copy(book_engine_list, queasy)

    return generate_output()