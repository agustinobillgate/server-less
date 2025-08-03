#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 3/8/2025
# if bediener
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Res_history, Bediener

def benutzer_zugriffbl(ch:string, nr:int, username:string, permissions:string, rec_id:int):

    prepare_cache ([Res_history, Bediener])

    res_history = bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_history, bediener
        nonlocal ch, nr, username, permissions, rec_id

        return {}

    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.action = "User Access"
    res_history.aenderung = "CHG Access Right of: " + username + " " +\
            permissions + "->" + ch


    pass
    pass

    bediener = get_cache (Bediener, {"_recid": [(eq, rec_id)]})
    if bediener:
        bediener.permissions = ch
    pass

    return generate_output()