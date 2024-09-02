from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Zimkateg, Bediener, Res_history

def update_dynaratecode_update_ratecodebl(rate_list1:[Rate_list1], rmtype:str, from_date:date, to_date:date, inp_str:str, user_init:str):
    inp_zikatnr:int = 0
    currcode:str = ""
    bookengid:int = 0
    lastrcode:str = ""
    queasy = zimkateg = bediener = res_history = None

    rate_list1 = buffqueasy = qsy = bqueasy = None

    rate_list1_list, Rate_list1 = create_model("Rate_list1", {"origcode":str, "counter":int, "w_day":int, "rooms":str, "rcode":str})

    Buffqueasy = Queasy
    Qsy = Queasy
    Bqueasy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal inp_zikatnr, currcode, bookengid, lastrcode, queasy, zimkateg, bediener, res_history
        nonlocal buffqueasy, qsy, bqueasy


        nonlocal rate_list1, buffqueasy, qsy, bqueasy
        nonlocal rate_list1_list
        return {}

    def update_ratecode():

        nonlocal inp_zikatnr, currcode, bookengid, lastrcode, queasy, zimkateg, bediener, res_history
        nonlocal buffqueasy, qsy, bqueasy


        nonlocal rate_list1, buffqueasy, qsy, bqueasy
        nonlocal rate_list1_list

        curr_date:date = None
        curr_i:int = 0

        for rate_list1 in query(rate_list1_list):
            curr_i = 0
            for curr_date in range(from_date,to_date + 1) :
                curr_i = curr_i + 1

                if rate_list1.rcode[curr_i - 1] == rate_list1.origcode:

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 145) &  (func.lower(Queasy.char1) == (currcode).lower()) &  (Queasy.char2 == rate_list1.origcode) &  (Queasy.number1 == inp_zikatnr) &  (Queasy.deci1 == rate_list1.w_day) &  (Queasy.deci2 == rate_list1.counter) &  (Queasy.date1 == curr_date)).first()

                    if queasy:
                        db_session.delete(queasy)

                elif rate_list1.rcode[curr_i - 1] != None:

                    if user_init != "":

                        bediener = db_session.query(Bediener).filter(
                                (func.lower(Bediener.userinit) == (user_init).lower())).first()

                        buffqueasy = db_session.query(Buffqueasy).filter(
                                (Buffqueasy.key == 145) &  (func.lower(Buffqueasy.char1) == (currcode).lower()) &  (Buffqueasy.char2 == rate_list1.origcode) &  (Buffqueasy.number1 == inp_zikatnr) &  (Buffqueasy.deci1 == rate_list1.w_day) &  (Buffqueasy.deci2 == rate_list1.counter) &  (Buffqueasy.date1 == curr_date)).first()

                        if buffqueasy:
                            lastrcode = buffqueasy.char3
                        res_history = Res_history()
                        db_session.add(res_history)

                        res_history.nr = bediener.nr
                        res_history.datum = get_current_date()
                        res_history.zeit = get_current_time_in_seconds()
                        res_history.action = "UpdateDynaRateCode"
                        res_history.aenderung = "RateCode: " + currcode + ", Occupancy: " + rate_list1.rooms + " Date: " + to_string(get_year(curr_date) , "9999") + to_string(get_month(curr_date) , "99") +\
                                to_string(get_day(curr_date) , "99") + "," + lastrcode + " ChangeTo " + rate_list1.rcode[curr_i - 1]

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 145) &  (func.lower(Queasy.char1) == (currcode).lower()) &  (Queasy.char2 == rate_list1.origcode) &  (Queasy.number1 == inp_zikatnr) &  (Queasy.deci1 == rate_list1.w_day) &  (Queasy.deci2 == rate_list1.counter) &  (Queasy.date1 == curr_date)).first()

                    if not queasy:
                        queasy = Queasy()
                        db_session.add(queasy)

                        queasy.key = 145
                        queasy.char1 = currcode
                        queasy.char2 = rate_list1.origcode
                        queasy.number1 = inp_zikatnr
                        queasy.deci1 = rate_list1.w_day
                        queasy.deci2 = rate_list1.counter
                        queasy.date1 = curr_date

                    queasy = db_session.query(Queasy).first()
                    queasy.char3 = rate_list1.rcode[curr_i - 1]
                    queasy.number2 = bediener.nr
                    queasy.number3 = get_current_time_in_seconds()
                    queasy.date2 = get_current_date()

                    queasy = db_session.query(Queasy).first()

    def update_bookengine_config():

        nonlocal inp_zikatnr, currcode, bookengid, lastrcode, queasy, zimkateg, bediener, res_history
        nonlocal buffqueasy, qsy, bqueasy


        nonlocal rate_list1, buffqueasy, qsy, bqueasy
        nonlocal rate_list1_list

        cm_gastno:int = 0
        datum:date = None
        iftask:str = ""
        mestoken:str = ""
        mesvalue:str = ""
        tokcounter:int = 0
        Qsy = Queasy
        Bqueasy = Queasy
        for datum in range(from_date,to_date + 1) :

            qsy = db_session.query(Qsy).filter(
                    (Qsy.key == 170) &  (Qsy.date1 == datum) &  (func.lower(Qsy.char1) == (currcode).lower()) &  (Qsy.logi1 == False) &  (Qsy.logi2 == False)).first()
            while None != qsy:

                bqueasy = db_session.query(Bqueasy).filter(
                        (Bqueasy._recid == qsy._recid)).first()

                if bqueasy:
                    bqueasy.logi2 = True

                    bqueasy = db_session.query(Bqueasy).first()


                qsy = db_session.query(Qsy).filter(
                        (Qsy.key == 170) &  (Qsy.date1 == datum) &  (func.lower(Qsy.char1) == (currcode).lower()) &  (Qsy.logi1 == False) &  (Qsy.logi2 == False)).first()

    if num_entries(inp_str, ";") > 1:
        currcode = entry(0, inp_str, ";")
        bookengid = to_int(entry(1, inp_str, ";"))


    else:
        currcode = inp_str

    if bookengid == 0:
        bookengid = 1

    zimkateg = db_session.query(Zimkateg).filter(
            (func.lower(Zimkateg.kurzbez) == (rmtype).lower())).first()

    if zimkateg:
        inp_zikatnr = zimkateg.zikatnr

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    update_ratecode()
    update_bookengine_config()

    return generate_output()