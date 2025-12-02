#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
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


    # queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, number1)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 159) &
             (Queasy.number1 == number1)).with_for_update().first()

    if queasy:
        pass
        db_session.delete(queasy)
        pass

    return generate_output()