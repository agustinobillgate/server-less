#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

category_data, Category = create_model("Category")

def egcategory_btn_exitbl(case_type:int, rec_id:int, category_data:[Category]):

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


    category = query(category_data, first=True)

    if case_type == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()

    elif case_type == 2:

        # queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy._recid == rec_id)).with_for_update().first()
        pass
        queasy.number1 = category.number1
        queasy.char1 = category.char1
        db_session.refresh(queasy,with_for_update=True)

    return generate_output()
