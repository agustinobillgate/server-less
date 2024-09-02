from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Ratecode, Zimkateg, Bediener, Res_history, Queasy

def delete_ratecodebl(case_type:int, int1:int, user_init:str):
    success_flag = False
    prcode:str = ""
    rmtype:str = ""
    chcode:str = ""
    startperiode:date = None
    endperiode:date = None
    wday:int = 0
    adult:int = 0
    rmcode:int = 0
    price:str = ""
    ratecode = zimkateg = bediener = res_history = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, prcode, rmtype, chcode, startperiode, endperiode, wday, adult, rmcode, price, ratecode, zimkateg, bediener, res_history, queasy


        return {"success_flag": success_flag}


    if case_type == 1:

        ratecode = db_session.query(Ratecode).filter(
                (Ratecode._recid == int1)).first()

        if ratecode:

            ratecode = db_session.query(Ratecode).first()

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == ratecode.zikatnr)).first()

            if zimkateg:
                rmcode = ratecode.zikatnr
                rmtype = zimkateg.kurzbez


            prcode = ratecode.CODE
            startperiode = ratecode.startperiode
            endperiode = ratecode.endperiode
            wday = ratecode.wday
            adult = ratecode.erwachs
            price = to_string(ratecode.zipreis)


            db_session.delete(ratecode)


            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Delete RateCode, Code: " + prcode + " rmtype : " + rmtype + " Start:" + to_string(startperiode) +\
                        "|End:" + to_string(endperiode) + "|DW" + to_string(wday) + "|adult:" + to_string(adult) + "|Rate:" + price
                res_history.action = "RateCode"

                res_history = db_session.query(Res_history).first()


        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (not Queasy.logi2) &  (num_entries(Queasy.char3, ";") > 2) &  (entry(1, Queasy.char3, ";") == (prcode).lower())).all():
            chcode = queasy.char1

            ratecode = db_session.query(Ratecode).filter(
                    (Ratecode.CODE == queasy.char1) &  (Ratecode.startperiode == startperiode) &  (Ratecode.endperiode == endperiode) &  (Ratecode.wday == wday) &  (Ratecode.erwachs == adult) &  (Ratecode.zikatnr == rmcode)).first()

            if ratecode:

                ratecode = db_session.query(Ratecode).first()
                db_session.delete(ratecode)


            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Delete Child RateCode, Code: " + chcode + " rmtype : " + rmtype
                res_history.action = "RateCode"

                res_history = db_session.query(Res_history).first()


    return generate_output()