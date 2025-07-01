#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def bookengine_admin_btn_deletebl(number1:int):
    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal number1

        return {}


    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, number1)]})

    if queasy:
        pass
        db_session.delete(queasy)
        pass

    return generate_output()