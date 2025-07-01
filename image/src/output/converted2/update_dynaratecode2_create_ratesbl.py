#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimkateg, Ratecode, Queasy

dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"counter":int, "rcode":string, "w_day":int, "fr_room":int, "to_room":int, "days1":int, "days2":int, "s_recid":int, "rmtype":string})

def update_dynaratecode2_create_ratesbl(dynarate_list_list:[Dynarate_list], rmtype:string, currcode:string, from_date:date, to_date:date, market_number:int):

    prepare_cache ([Zimkateg, Queasy])

    rate_list1_list = []
    curr_date:date = None
    i:int = 0
    curr_i:int = 0
    w_day:int = 0
    inp_zikatnr:int = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    zimkateg = ratecode = queasy = None

    rate_list1 = dynarate_list = None

    rate_list1_list, Rate_list1 = create_model("Rate_list1", {"origcode":string, "counter":int, "w_day":int, "rooms":string, "rcode":[string,31]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rate_list1_list, curr_date, i, curr_i, w_day, inp_zikatnr, wd_array, zimkateg, ratecode, queasy
        nonlocal rmtype, currcode, from_date, to_date, market_number


        nonlocal rate_list1, dynarate_list
        nonlocal rate_list1_list

        return {"rate-list1": rate_list1_list}


    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmtype)]})

    if zimkateg:
        inp_zikatnr = zimkateg.zikatnr

    for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  == (rmtype).lower()), sort_by=[("w_day",False),("fr_room",False),("days1",False),("days2",False)]):
        rate_list1 = Rate_list1()
        rate_list1_list.append(rate_list1)

        rate_list1.counter = dynarate_list.counter
        rate_list1.origcode = dynarate_list.rcode
        rate_list1.w_day = dynarate_list.w_day
        rate_list1.rooms = to_string(dynarate_list.fr_room) +\
                "-" + to_string(dynarate_list.to_room)


        curr_date = from_date - timedelta(days=1)
        i = 0
        for curr_i in range(get_day(from_date),get_day(to_date)  + 1) :
            i = i + 1
            curr_date = curr_date + timedelta(days=1)
            w_day = wd_array[get_weekday(curr_date) - 1]

            if dynarate_list.w_day > 0 and dynarate_list.w_day != w_day:
                rate_list1.rcode[i - 1] = None
            else:
                pass

                if zimkateg:

                    ratecode = get_cache (Ratecode, {"code": [(eq, dynarate_list.rcode)],"startperiode": [(le, to_date)],"endperiode": [(ge, from_date)],"zikatnr": [(eq, inp_zikatnr)],"marknr": [(eq, market_number)]})
                else:

                    ratecode = get_cache (Ratecode, {"code": [(eq, dynarate_list.rcode)],"startperiode": [(le, curr_date)],"endperiode": [(ge, curr_date)],"marknr": [(eq, market_number)]})

                if not ratecode:
                    rate_list1.rcode[i - 1] = None
                else:
                    rate_list1.rcode[i - 1] = dynarate_list.rcode

                    queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, currcode)],"char2": [(eq, rate_list1.origcode)],"number1": [(eq, inp_zikatnr)],"deci1": [(eq, dynarate_list.w_day)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, curr_date)]})

                    if queasy:
                        rate_list1.rcode[i - 1] = queasy.char3

    return generate_output()