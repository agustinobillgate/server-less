#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy, Bediener

rmlist_data, Rmlist = create_model("Rmlist", {"flag":int, "code":string, "zinr":string, "credit":int, "floor":int, "gname":string, "pic":string, "bemerk":string, "rstat":string, "ankunft":date, "abreise":date, "kbezeich":string, "nation":string, "paxnr":int})

def hk_rmboy_send_to_mobilebl(rmlist_data:[Rmlist]):

    prepare_cache ([Htparam, Bediener])

    success_flag = False
    user_init:string = ""
    ci_date:date = None
    htparam = queasy = bediener = None

    rmlist = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, user_init, ci_date, htparam, queasy, bediener


        nonlocal rmlist

        return {"success_flag": success_flag}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 196) & (Queasy.date1 == ci_date) & (Queasy.char2 == "") & (Queasy.number1 == 0) & (Queasy.number2 == 0)).order_by(Queasy._recid).with_for_update().all():
        db_session.delete(queasy)

    for rmlist in query(rmlist_data, sort_by=[("pic",False)]):

        bediener = get_cache (Bediener, {"username": [(eq, rmlist.pic)]})

        if bediener:
            user_init = bediener.userinit


        else:
            user_init = " "

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 196) & (entry(0, Queasy.char1, ";") == rmlist.zinr) & (Queasy.date1 == ci_date)).with_for_update().first()

        if queasy:
            queasy.char1 = " "
            queasy.char1 = rmlist.zinr + ";" + user_init + ";" + to_string(rmlist.credit)
            queasy.char2 = ""
            queasy.number1 = 0
            queasy.number2 = 0


            pass
            pass
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 196
            queasy.char1 = rmlist.zinr + ";" + user_init + ";" + to_string(rmlist.credit)
            queasy.date1 = ci_date


    success_flag = True

    return generate_output()