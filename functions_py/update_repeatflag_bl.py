#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 12/11/2025
# CM, dipanggil dari bookengine_config_btn_exit_2bl.py
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def update_repeatflag_bl():

    prepare_cache ([Queasy])

    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy

        return {}


    queasy = get_cache (Queasy, {"key": [(eq, 167)]})

    if queasy:
        pass
        queasy.date1 = get_current_date()
        queasy.logi1 = True
        pass
    else:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 167
        queasy.date1 = get_current_date()
        queasy.logi1 = True

    return generate_output()