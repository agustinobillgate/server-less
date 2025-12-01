#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 12/11/2025
# CM
#---------------------------------------
# Rd, 27/11/2025, with_for_update added
#------------------------------------------
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

    # queasy = get_cache (Queasy, {"key": [(eq, 167)],"number1": [(eq, bookengid)]})
    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 167) &
             (Queasy.number1 == bookengid)).with_for_update().first()

    if queasy:
        queasy.date1 = get_current_date()
        queasy.logi1 = True
        pass

    return generate_output()