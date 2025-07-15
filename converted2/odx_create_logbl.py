#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def odx_create_logbl(rechnr:int, dept:int, content:string, body:string, response:string):

    prepare_cache ([Queasy])

    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal rechnr, dept, content, body, response

        return {}

    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 242
    queasy.number1 = 99
    queasy.number2 = rechnr
    queasy.number3 = dept
    queasy.date1 = get_current_date()
    queasy.deci1 =  to_decimal(get_current_time_in_seconds)()
    queasy.char1 = content
    queasy.char2 = body
    queasy.char3 = response

    return generate_output()