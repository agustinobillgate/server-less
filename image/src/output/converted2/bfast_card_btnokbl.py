#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Mealcoup, Queasy, Bediener, Res_history

def bfast_card_btnokbl(resnr:int, failreadflag:bool, user_init:string, roomnr:string, consumeuse:int, mealtime:string, cidate:date, codate:date):

    prepare_cache ([Htparam, Mealcoup, Queasy, Bediener, Res_history])

    resultstr = ""
    p_87:date = None
    num_of_day:int = 0
    diffcidate:int = 0
    i:int = 0
    htparam = mealcoup = queasy = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resultstr, p_87, num_of_day, diffcidate, i, htparam, mealcoup, queasy, bediener, res_history
        nonlocal resnr, failreadflag, user_init, roomnr, consumeuse, mealtime, cidate, codate

        return {"resultstr": resultstr}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        p_87 = htparam.fdate
    diffcidate = (p_87 - cidate).days

    if diffcidate > 32:
        num_of_day = diffcidate - 32
    else:
        num_of_day = diffcidate

    if num_of_day >= 0:

        mealcoup = get_cache (Mealcoup, {"resnr": [(eq, resnr)],"zinr": [(eq, roomnr)],"name": [(eq, mealtime)]})

        if mealcoup:
            pass
            mealcoup.verbrauch[num_of_day - 1] = mealcoup.verbrauch[num_of_day - 1] + consumeuse

            if diffcidate > 32 and (diffcidate - 32 == 1):
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 176
                queasy.number1 = mealcoup._recid
                queasy.number2 = mealcoup.resnr
                queasy.number3 = (diffcidate - (diffcidate % 32)) / 32


                for i in range(1,length(mealcoup.verbrauch)  + 1) :
                    queasy.char1 = to_string(mealcoup.verbrauch[i - 1]) + ";"


            pass
            pass
        else:
            mealcoup = Mealcoup()
            db_session.add(mealcoup)

            mealcoup.resnr = resnr
            mealcoup.zinr = roomnr
            mealcoup.name = mealtime
            mealcoup.verbrauch[num_of_day - 1] = consumeuse
            mealcoup.ankunft = cidate
            mealcoup.abreise = codate


        resultstr = "Success"

        if failreadflag:

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "ReadCard:Failure read from encoder, user " +\
                    bediener.username + " trying to querying room number manually"


            res_history.action = "BreakfastKey"
            pass
            pass

        return generate_output()
    resultstr = "Failed"

    return generate_output()