from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zimkateg, Ratecode, Queasy

def update_dynaratecode_create_ratesbl(dynarate_list:[Dynarate_list], rmtype:str, currcode:str, from_date:date, to_date:date, market_number:int):
    rate_list1_list = []
    curr_date:date = None
    curr_i:int = 0
    w_day:int = 0
    inp_zikatnr:int = 0
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    zimkateg = ratecode = queasy = None

    rate_list1 = dynarate_list = None

    rate_list1_list, Rate_list1 = create_model("Rate_list1", {"origcode":str, "counter":int, "w_day":int, "rooms":str, "rcode":str})
    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"counter":int, "rcode":str, "w_day":int, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rmtype":str, "s_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rate_list1_list, curr_date, curr_i, w_day, inp_zikatnr, wd_array, zimkateg, ratecode, queasy


        nonlocal rate_list1, dynarate_list
        nonlocal rate_list1_list, dynarate_list_list
        return {"rate-list1": rate_list1_list}


    zimkateg = db_session.query(Zimkateg).filter(
            (func.lower(Zimkateg.kurzbez) == (rmtype).lower())).first()

    if zimkateg:
        inp_zikatnr = zimkateg.zikatnr

    for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list :dynarate_list.(rmtype).lower().lower()  == (rmtype).lower())):
        rate_list1 = Rate_list1()
        rate_list1_list.append(rate_list1)

        rate_list1.counter = dynarate_list.counter
        rate_list1.origcode = dynarate_list.rcode
        rate_list1.w_day = dynarate_list.w_day
        rate_list1.rooms = to_string(dynaRate_list.fr_room) +\
                "-" + to_string(dynaRate_list.to_room)


        curr_date = from_date - 1
        for curr_i in range(1,get_day(to_date)  + 1) :
            curr_date = curr_date + 1
            w_day = wd_array[get_weekday(curr_date) - 1]

            if dynarate_list.w_day > 0 and dynarate_list.w_day != w_day:
                rate_list1.rcode[curr_i - 1] = None
            else:


                if zimkateg:

                    ratecode = db_session.query(Ratecode).filter(
                            (Ratecode.CODE == dynarate_list.rCode) &  (Ratecode.startperiode <= curr_date) &  (Ratecode.endperiode >= curr_date) &  (Ratecode.zikatnr == inp_zikatnr) &  (Ratecode.marknr == market_number)).first()
                else:

                    ratecode = db_session.query(Ratecode).filter(
                            (Ratecode.CODE == dynarate_list.rCode) &  (Ratecode.startperiode <= curr_date) &  (Ratecode.endperiode >= curr_date) &  (Ratecode.marknr == market_number)).first()

                if not ratecode:
                    rate_list1.rcode[curr_i - 1] = None
                else:
                    rate_list1.rcode[curr_i - 1] = dynarate_list.rcode

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 145) &  (func.lower(Queasy.char1) == (currcode).lower()) &  (Queasy.char2 == rate_list1.origcode) &  (Queasy.number1 == inp_zikatnr) &  (Queasy.deci1 == dynarate_list.w_day) &  (Queasy.deci2 == dynarate_list.counter) &  (Queasy.date1 == curr_date)).first()

                    if queasy:
                        rate_list1.rcode[curr_i - 1] = queasy.char3

    return generate_output()