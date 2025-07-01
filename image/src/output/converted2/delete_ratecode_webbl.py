#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Ratecode, Zimkateg, Bediener, Res_history, Queasy

recid_list_list, Recid_list = create_model("Recid_list", {"int1":int})

def delete_ratecode_webbl(case_type:int, recid_list_list:[Recid_list], user_init:string):

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

    recid_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, prcode, rmtype, chcode, startperiode, endperiode, wday, adult, rmcode, price, ratecode, zimkateg, bediener, res_history, queasy
        nonlocal case_type, user_init


        nonlocal recid_list

        return {"success_flag": success_flag}

    if case_type == 1:

        for recid_list in query(recid_list_list):

            ratecode = get_cache (Ratecode, {"_recid": [(eq, recid_list.int1)]})

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
                pass

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Delete Multiple RateCode, Code: " + prcode + " rmtype : " + rmtype + " Start:" + to_string(startperiode) +\
                            "|End:" + to_string(endperiode) + "|DW" + to_string(wday) + "|adult:" + to_string(adult) + "|Rate:" + price
                    res_history.action = "RateCode"


                    pass
                    pass
                success_flag = True

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 2) & not_ (Queasy.logi2) & (num_entries(Queasy.char3, ";") > 2) & (entry(1, Queasy.char3, ";") == (prcode).lower())).order_by(Queasy._recid).all():
                chcode = queasy.char1

                ratecode = get_cache (Ratecode, {"code": [(eq, queasy.char1)],"startperiode": [(eq, startperiode)],"endperiode": [(eq, endperiode)],"wday": [(eq, wday)],"erwachs": [(eq, adult)],"zikatnr": [(eq, rmcode)]})

                if ratecode:
                    pass
                    db_session.delete(ratecode)
                    pass

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Auto Delete Child RateCode, Code: " + chcode + " rmtype : " + rmtype + " Parent : " + prcode
                    res_history.action = "RateCode"


                    pass
                    pass

    return generate_output()