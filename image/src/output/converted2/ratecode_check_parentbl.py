#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def ratecode_check_parentbl(intkey:int, inpchar1:string):
    check_parent = False
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal check_parent, queasy
        nonlocal intkey, inpchar1

        return {"check_parent": check_parent}


    queasy = get_cache (Queasy, {"key": [(eq, intkey)],"char1": [(eq, inpchar1)]})

    if not queasy:
        check_parent = True

    return generate_output()