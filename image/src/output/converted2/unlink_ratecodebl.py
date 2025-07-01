#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def unlink_ratecodebl(child_code:string, tb1_char3:string):

    prepare_cache ([Queasy])

    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal child_code, tb1_char3

        return {}


    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, child_code)]})
    queasy.char3 = tb1_char3


    pass

    return generate_output()