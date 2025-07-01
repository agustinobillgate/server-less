#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def eg_action_maintaskbl(maintask:int):

    prepare_cache ([Queasy])

    do_it = False
    char1 = ""
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, char1, queasy
        nonlocal maintask

        return {"do_it": do_it, "char1": char1}


    queasy = get_cache (Queasy, {"key": [(eq, 133)],"number1": [(eq, maintask)]})

    if not queasy:
        do_it = True
    else:
        char1 = queasy.char1

    return generate_output()