#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy, Bediener, Zimmer

def hk_rmboy_starttimebl(userinit:string, zinr:string):

    prepare_cache ([Htparam, Queasy, Bediener, Zimmer])

    msg_str = ""
    ci_date:date = None
    do_it:bool = False
    room:string = ""
    htparam = queasy = bediener = zimmer = None

    db_session = local_storage.db_session
    zinr = zinr.strip()

    def generate_output():
        nonlocal msg_str, ci_date, do_it, room, htparam, queasy, bediener, zimmer
        nonlocal userinit, zinr

        return {"msg_str": msg_str}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    do_it = True

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 196) & (Queasy.date1 == ci_date) & (Queasy.char2 == (userinit).lower())).order_by(Queasy._recid).all():

        if queasy.number1 != 0 and queasy.number2 == 0:
            do_it = False
            room = entry(0, queasy.char1, ";")

    if not do_it:
        msg_str = "Ongoing Cleaning room Exist, Start Cleaning Another room Is Not Allowed!-" + room

        return generate_output()

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 196) & (Queasy.date1 == ci_date) & (entry(0, Queasy.char1, ";") == (zinr).lower())).with_for_update().first()

    if queasy:

        if queasy.char2 != "" and queasy.number1 != 0:

            bediener = get_cache (Bediener, {"userinit": [(eq, queasy.char2)]})

            if bediener:

                if queasy.number2 == 0:
                    msg_str = "room " + zinr + " is being cleaned by " + bediener.username

                    return generate_output()
                else:

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})

                    if zimmer and zimmer.zistatus <= 1:
                        msg_str = "room " + zinr + " is already cleaned by " + bediener.username

                        return generate_output()
        queasy.char2 = userinit
        queasy.number1 = get_current_time_in_seconds()
        queasy.number2 = 0
    pass
    pass

    return generate_output()