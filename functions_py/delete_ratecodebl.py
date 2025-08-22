#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 13/8/2025
# num_entries, db_commit()
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Ratecode, Zimkateg, Bediener, Res_history, Queasy

def delete_ratecodebl(case_type:int, int1:int, user_init:string):

    prepare_cache ([Zimkateg, Bediener, Res_history, Queasy])

    success_flag = False
    prcode:string = ""
    rmtype:string = ""
    chcode:string = ""
    startperiode:date = None
    endperiode:date = None
    wday:int = 0
    adult:int = 0
    rmcode:int = 0
    price:string = ""
    ratecode = zimkateg = bediener = res_history = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, prcode, rmtype, chcode, startperiode, endperiode, wday, adult, rmcode, price, ratecode, zimkateg, bediener, res_history, queasy
        nonlocal case_type, int1, user_init

        return {"success_flag": success_flag}


    if case_type == 1:

        ratecode = get_cache (Ratecode, {"_recid": [(eq, int1)]})

        if ratecode:
            pass

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, ratecode.zikatnr)]})

            if zimkateg:
                rmcode = ratecode.zikatnr
                rmtype = zimkateg.kurzbez


            prcode = ratecode.code
            startperiode = ratecode.startperiode
            endperiode = ratecode.endperiode
            wday = ratecode.wday
            adult = ratecode.erwachs
            price = to_string(ratecode.zipreis)


            db_session.delete(ratecode)
            # Rd 15/8/2025
            db_session.commit()
            pass

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Delete RateCode, Code: " + prcode + " rmtype : " + rmtype + " Start:" + to_string(startperiode) +\
                        "|End:" + to_string(endperiode) + "|DW" + to_string(wday) + "|adult:" + to_string(adult) + "|Rate:" + price
                res_history.action = "RateCode"


                pass
                pass
        
        # Rd, 13/8/2025
        # for queasy in db_session.query(Queasy).filter(
        #          (Queasy.key == 2) & not_ (Queasy.logi2) & (num_entries(Queasy.char3, ";") > 2) & (entry(1, Queasy.char3, ";") == (prcode).lower())).order_by(Queasy._recid).all():
        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 2) & not_ (Queasy.logi2) &  
                 (entry(1, Queasy.char3, ";") == (prcode).lower())).order_by(Queasy._recid).all():
            if (num_entries(queasy.char3, ";") > 2):
                chcode = queasy.char1

                ratecode = get_cache (Ratecode, {"code": [(eq, queasy.char1)],"startperiode": [(eq, startperiode)],"endperiode": [(eq, endperiode)],"wday": [(eq, wday)],"erwachs": [(eq, adult)],"zikatnr": [(eq, rmcode)]})

                if ratecode:
                    pass
                    db_session.delete(ratecode)
                    # Rd 15/8/2025
                    db_session.commit()
                    pass

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Delete Child RateCode, Code: " + chcode + " rmtype : " + rmtype
                    res_history.action = "RateCode"
                    # Rd 15/8/2025
                    db_session.commit()

                    pass
                    pass

    return generate_output()