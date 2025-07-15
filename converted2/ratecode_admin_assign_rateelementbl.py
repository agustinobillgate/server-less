#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def ratecode_admin_assign_rateelementbl(prcode:string):

    prepare_cache ([Queasy])

    rcode_element = ""
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rcode_element, queasy
        nonlocal prcode

        return {"rcode_element": rcode_element}


    queasy = get_cache (Queasy, {"key": [(eq, 289)],"char1": [(eq, prcode)]})

    if queasy:
        rcode_element = queasy.char2

    return generate_output()