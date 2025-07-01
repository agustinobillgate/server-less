#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def egsource_source_charbl(curr_select:string, source_char1:string):

    prepare_cache ([Queasy])

    err_code = 0
    queasy = None

    queasy1 = None

    Queasy1 = create_buffer("Queasy1",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, queasy
        nonlocal curr_select, source_char1
        nonlocal queasy1


        nonlocal queasy1

        return {"err_code": err_code}


    if curr_select.lower()  == ("chg").lower() :

        queasy1 = get_cache (Queasy, {"char1": [(eq, source_char1)],"number2": [(eq, 0)],"deci2": [(eq, 0)],"key": [(eq, 130)],"_recid": [(ne, queasy._recid)]})

    elif curr_select.lower()  == ("add").lower() :

        queasy1 = get_cache (Queasy, {"char1": [(eq, source_char1)],"deci2": [(eq, 0)],"key": [(eq, 130)]})

    if queasy1:
        err_code = 1

    return generate_output()