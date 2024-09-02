from functions.additional_functions import *
import decimal
from models import Queasy

def egcategory_btn_exitbl(case_type:int, rec_id:int, category:[Category]):
    queasy = None

    category = None

    category_list, Category = create_model("Category")


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        nonlocal category
        nonlocal category_list
        return {}

    def fill_new_queasy():

        nonlocal queasy


        nonlocal category
        nonlocal category_list


        queasy.key = 132
        queasy.number1 = category.number1
        queasy.char1 = category.char1

    category = query(category_list, first=True)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()

    elif case_type == 2:

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == rec_id)).first()

        queasy = db_session.query(Queasy).first()
        queasy.number1 = category.number1
        queasy.char1 = category.char1

        queasy = db_session.query(Queasy).first()

    return generate_output()