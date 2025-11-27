#using conversion tools version: 1.0.0.117
# #-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Zimkateg, Bediener, Res_history

def update_allotmentbyrate2bl(from_date:date, to_date:date, allotment:int, inp_str:string, rmtype:string):

    prepare_cache ([Zimkateg, Bediener, Res_history])

    datum:date = None
    cat_flag:bool = False
    i_typ:int = 0
    currcode:string = ""
    user_init:string = ""
    created:bool = False
    avail_qsy:bool = False
    betribnr:int = 0
    queasy = zimkateg = bediener = res_history = None

    db_session = local_storage.db_session
    inp_str = inp_str.strip()
    rmtype = rmtype.strip()

    def generate_output():
        nonlocal datum, cat_flag, i_typ, currcode, user_init, created, avail_qsy, betribnr, queasy, zimkateg, bediener, res_history
        nonlocal from_date, to_date, allotment, inp_str, rmtype

        return {}


    if num_entries(inp_str, ";") > 1:
        currcode = entry(0, inp_str, ";")
        user_init = entry(1, inp_str, ";")


    else:
        currcode = inp_str

    queasy = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(eq, "")]})

    if queasy:
        betribnr = queasy.betriebsnr

    queasy = get_cache (Queasy, {"key": [(eq, 152)],"char1": [(eq, rmtype)]})

    if queasy:
        i_typ = queasy.number1

    elif not queasy:

        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmtype)]})

        if zimkateg:
            i_typ = zimkateg.zikatnr
    for datum in date_range(from_date,to_date) :
        avail_qsy = False

        if user_init != "":
            created = True

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "UpdateAllotmentByRateCode"

        if allotment != 0:

            # queasy = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(eq, currcode)],"date1": [(eq, datum)],"number1": [(eq, i_typ)]})
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) &
                     (Queasy.char1 == currcode) &
                     (Queasy.date1 == datum) &
                     (Queasy.number1 == i_typ)).with_for_update().first()

            if queasy and queasy.number3 != allotment:

                if user_init != "":
                    res_history.aenderung = "RCode:" + currcode + ",rmtype:" + rmtype + "Date: " + to_string(get_year(datum) , "9999") + to_string(get_month(datum) , "99") + to_string(get_day(datum) , "99") + "," + to_string(queasy.number3) + " ChangeTo " + to_string(allotment)
                pass
                queasy.number3 = allotment
                queasy.logi3 = True


                pass
                pass

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
                queasy.betriebsnr = betribnr

                if user_init != "":
                    res_history.aenderung = "RCode:" + currcode + ",rmtype:" + rmtype + "Date: " + to_string(get_year(datum) , "9999") + to_string(get_month(datum) , "99") + to_string(get_day(datum) , "99") + ", All ChangeTo " + to_string(allotment)

        elif allotment == 0:

            # queasy = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(eq, currcode)],"date1": [(eq, datum)],"number1": [(eq, i_typ)]})
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 171) &
                     (Queasy.char1 == currcode) &
                     (Queasy.date1 == datum) &
                     (Queasy.number1 == i_typ)).with_for_update().first()

            if queasy and queasy.number3 != allotment:
                avail_qsy = True
                pass
                db_session.delete(queasy)
                pass

            if avail_qsy:

                # queasy = get_cache (Queasy, {"key": [(eq, 171)],"char1": [(eq, "")],"date1": [(eq, datum)],"number1": [(eq, i_typ)],"betriebsnr": [(eq, betribnr)]})
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 171) &
                         (Queasy.char1 == "") &
                         (Queasy.date1 == datum) &
                         (Queasy.number1 == i_typ) &
                         (Queasy.betriebsnr == betribnr)).with_for_update().first()
                if queasy and queasy.logi1 == False and queasy.logi2 == False and queasy.logi3 == False:
                    pass
                    queasy.logi1 = True


                    pass
                    pass

    return generate_output()