#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def egcategory_catcharbl(curr_select:string, category_char1:string, rec_id:int):

    prepare_cache ([Queasy])

    avail_queasy = False
    queasy = None

    queasy1 = None

    Queasy1 = create_buffer("Queasy1",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_queasy, queasy
        nonlocal curr_select, category_char1, rec_id
        nonlocal queasy1


        nonlocal queasy1

        return {"avail_queasy": avail_queasy}


    queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})

    if curr_select.lower()  == ("chg").lower() :

        queasy1 = get_cache (Queasy, {"char1": [(eq, category_char1)],"number2": [(eq, 0)],"deci2": [(eq, 0)],"key": [(eq, 132)],"_recid": [(ne, queasy._recid)]})

    elif curr_select.lower()  == ("add").lower() :

        queasy1 = get_cache (Queasy, {"char1": [(eq, category_char1)],"number2": [(eq, 0)],"deci2": [(eq, 0)],"key": [(eq, 132)]})

    if queasy1:
        avail_queasy = True

    return generate_output()