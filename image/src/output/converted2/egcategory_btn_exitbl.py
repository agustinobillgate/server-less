#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

category_list, Category = create_model("Category")

def egcategory_btn_exitbl(case_type:int, rec_id:int, category_list:[Category]):

    prepare_cache ([Queasy])

    queasy = None

    category = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal case_type, rec_id


        nonlocal category

        return {}

    def fill_new_queasy():

        nonlocal queasy
        nonlocal case_type, rec_id


        nonlocal category


        queasy.key = 132
        queasy.number1 = category.number1
        queasy.char1 = category.char1


    category = query(category_list, first=True)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()

    elif case_type == 2:

        queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
        pass
        queasy.number1 = category.number1
        queasy.char1 = category.char1
        pass

    return generate_output()