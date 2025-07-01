#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy, Bediener

def hk_rmboy_set_durationbl(userinit:string, zinr:string, duration:int):

    prepare_cache ([Htparam, Queasy, Bediener])

    msg_str = ""
    ci_date:date = None
    htparam = queasy = bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, ci_date, htparam, queasy, bediener
        nonlocal userinit, zinr, duration

        return {"msg_str": msg_str}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 196) & (Queasy.date1 == ci_date) & (entry(0, Queasy.char1, ";") == (zinr).lower())).first()

    if queasy:

        if queasy.char2.lower()  == (userinit).lower() :
            queasy.number2 = get_current_time_in_seconds()
        else:

            bediener = get_cache (Bediener, {"userinit": [(eq, queasy.char2)]})

            if bediener:

                if to_int(substring(bediener.permissions, 81, 1)) >= 2:
                    queasy.number2 = get_current_time_in_seconds()
                else:
                    msg_str = "Room " + zinr + " is being cleaned by " + bediener.username
    pass
    pass

    return generate_output()