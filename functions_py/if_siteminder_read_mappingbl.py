#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def if_siteminder_read_mappingbl(icase:int, p_char:string):

    prepare_cache ([Queasy])

    n_char = ""
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal n_char, queasy
        nonlocal icase, p_char

        return {"n_char": n_char}

    n_char = p_char

    if icase == 1:

        queasy = get_cache (Queasy, {"key": [(eq, 164)],"char2": [(ne, ""),(eq, p_char)]})

        if queasy:
            n_char = queasy.char1
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 165)],"char2": [(ne, ""),(eq, p_char)]})

        if queasy:
            n_char = queasy.char1

    return generate_output()