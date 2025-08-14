#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 14/8/2025
# if available bqueasy
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history, Guestbook

def hk_del_lostfoundbl(userinit:string, rec_id:int):

    prepare_cache ([Bediener, Res_history])

    curr_nr:int = 0
    queasy = bediener = res_history = guestbook = None

    bqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_nr, queasy, bediener, res_history, guestbook
        nonlocal userinit, rec_id
        nonlocal bqueasy


        nonlocal bqueasy

        return {}


    bediener = get_cache (Bediener, {"userinit": [(eq, userinit)]})

    if bediener:

        queasy = get_cache (Queasy, {"_recid": [(eq, rec_id)]})

        if queasy:
            curr_nr = queasy.number3


            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Delete LostFound No" +\
                    to_string(queasy.number3, ">>>9") +\
                    " Room " + queasy.char1


            res_history.action = "HouseKeeping"
            pass
            pass
            pass
            db_session.delete(queasy)
            pass

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 195) & (Queasy.char1 == ("LostAndFound;nr=" + to_string(curr_nr).lower()))).order_by(Queasy._recid).all():

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, queasy.number1)]})

        if guestbook:
            pass
            db_session.delete(guestbook)
            pass

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).first()
        # Rd 14/8/2025
        if bqueasy:
            db_session.delete(bqueasy)
        pass

    return generate_output()