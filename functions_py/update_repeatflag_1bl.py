#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 12/11/2025
# CM
#---------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def update_repeatflag_1bl(bookengid:int):

    prepare_cache ([Queasy])
    queasy = None
    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal bookengid

        return {}

    queasy = get_cache (Queasy, {"key": [(eq, 167)],"number1": [(eq, bookengid)]})

    if queasy:
        queasy.date1 = get_current_date()
        queasy.logi1 = True
        pass

    return generate_output()