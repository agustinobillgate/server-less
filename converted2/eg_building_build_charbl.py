#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def eg_building_build_charbl(curr_select:string, build_char1:string):

    prepare_cache ([Queasy])

    avail_queasy = False
    queasy = None

    queasy1 = None

    Queasy1 = create_buffer("Queasy1",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_queasy, queasy
        nonlocal curr_select, build_char1
        nonlocal queasy1


        nonlocal queasy1

        return {"avail_queasy": avail_queasy}


    if curr_select.lower()  == ("chg").lower() :

        queasy1 = get_cache (Queasy, {"char1": [(eq, build_char1)],"number2": [(eq, 0)],"deci2": [(eq, 0)],"key": [(eq, 135)],"_recid": [(ne, queasy._recid)]})

    elif curr_select.lower()  == ("add").lower() :

        queasy1 = get_cache (Queasy, {"char1": [(eq, build_char1)],"number2": [(eq, 0)],"deci2": [(eq, 0)],"key": [(eq, 135)]})

    if queasy1:
        avail_queasy = True

    return generate_output()