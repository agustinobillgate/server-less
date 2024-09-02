from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Zimkateg, Bediener, Res_history

def update_allotmentbyrate2bl(from_date:date, to_date:date, allotment:int, inp_str:str, rmtype:str):
    datum:date = None
    cat_flag:bool = False
    i_typ:int = 0
    currcode:str = ""
    user_init:str = ""
    created:bool = False
    avail_qsy:bool = False
    queasy = zimkateg = bediener = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum, cat_flag, i_typ, currcode, user_init, created, avail_qsy, queasy, zimkateg, bediener, res_history


        return {}


    if num_entries(inp_str, ";") > 1:
        currcode = entry(0, inp_str, ";")
        user_init = entry(1, inp_str, ";")


    else:
        currcode = inp_str

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 152) &  (func.lower(Queasy.char1) == (rmtype).lower())).first()

    if queasy:
        i_typ = queasy.number1

    elif not queasy:

        zimkateg = db_session.query(Zimkateg).filter(
                (func.lower(Zimkateg.kurzbez) == (rmtype).lower())).first()

        if zimkateg:
            i_typ = zimkateg.zikatnr
    for datum in range(from_date,to_date + 1) :
        avail_qsy = False

        if user_init != "":
            created = True

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "AllotmentByRateCode"

        if allotment != 0:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 171) &  (func.lower(Queasy.char1) == (currcode).lower()) &  (Queasy.date1 == datum) &  (Queasy.number1 == i_typ)).first()

            if queasy and queasy.number3 != allotment:

                if user_init != "":
                    res_history.aenderung = "RCode:" + currcode + ",rmtype:" + rmtype + "Date: " + to_string(get_year(datum) , "9999") + to_string(get_month(datum) , "99") + to_string(get_day(datum) , "99") + "," + to_string(queasy.number3) + "ChangeTo" + to_string(allotment)

                queasy = db_session.query(Queasy).first()
                queasy.number3 = allotment
                queasy.logi3 = True

                queasy = db_session.query(Queasy).first()


            elif not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 171
                queasy.char1 = currcode
                queasy.number1 = i_typ
                queasy.number3 = allotment
                queasy.date1 = datum
                queasy.logi1 = True
                queasy.logi3 = True

                if user_init != "":
                    res_history.aenderung = "RCode:" + currcode + ",rmtype:" + rmtype + "Date: " + to_string(get_year(datum) , "9999") + to_string(get_month(datum) , "99") + to_string(get_day(datum) , "99") + ",All ChangeTo" + to_string(allotment)

        elif allotment == 0:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 171) &  (func.lower(Queasy.char1) == (currcode).lower()) &  (Queasy.date1 == datum) &  (Queasy.number1 == i_typ)).first()

            if queasy and queasy.number3 != allotment:
                avail_qsy = True

                queasy = db_session.query(Queasy).first()
                db_session.delete(queasy)


            if avail_qsy:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 171) &  (Queasy.char1 == "") &  (Queasy.date1 == datum) &  (Queasy.number1 == i_typ)).first()

                if queasy and queasy.logi1 == False and queasy.logi2 == False and queasy.logi3 == False:

                    queasy = db_session.query(Queasy).first()
                    queasy.logi3 = True

                    queasy = db_session.query(Queasy).first()


    return generate_output()