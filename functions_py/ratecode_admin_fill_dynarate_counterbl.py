#using conversion tools version: 1.0.0.119
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Counters, Ratecode, Queasy, Zimkateg

def ratecode_admin_fill_dynarate_counterbl(r_code:string, dynarate_list_rmtype:string, dynarate_list_rcode:string, dynarate_list_w_day:int):

    prepare_cache ([Counters, Ratecode, Queasy, Zimkateg])

    curr_counter = 0
    counters = ratecode = queasy = zimkateg = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_counter, counters, ratecode, queasy, zimkateg
        nonlocal r_code, dynarate_list_rmtype, dynarate_list_rcode, dynarate_list_w_day

        return {"curr_counter": curr_counter}

    def fill_dynarate_counter():

        nonlocal curr_counter, counters, ratecode, queasy, zimkateg
        nonlocal r_code, dynarate_list_rmtype, dynarate_list_rcode, dynarate_list_w_day

        # Rd, 24/11/2025, Update last counter dengan next_counter_for_update
        # counters = get_cache (Counters, {"counter_no": [(eq, 50)]})
        counters = db_session.query(Counters).filter(
                 (Counters.counter_no == 50)).with_for_update().first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 50
            counters.counter_bez = "Counter for Dynamic Ratecode"
            counters.counter = 0


        counters.counter = counters.counter + 1
        pass
        curr_counter = counters.counter

        ratecode = get_cache (Ratecode, {"code": [(eq, r_code)]})
        pass
        ratecode.char1[4] = "CN" + to_string(curr_counter) + ";" +\
                ratecode.char1[4]


        pass

        if dynarate_list_rmtype.lower()  == ("*").lower() :

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 145) & (Queasy.char1 == ratecode.code) & (Queasy.char2 == dynarate_list_rcode) & (Queasy.number1 == 0) & (Queasy.deci1 == dynarate_list_w_day)).order_by(Queasy._recid).all():
                queasy.deci2 =  to_decimal(curr_counter)

        else:
            # Rulita, 19-11-2025
            # zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, dynarate_list_rmtype)]})
            zimkateg = db_session.query(Zimkateg).filter(
                            Zimkateg.kurzbez == dynarate_list_rmtype).first()
            if zimkateg : 
                for queasy in db_session.query(Queasy).filter(
                        (Queasy.key == 145) & (Queasy.char1 == ratecode.code) & (Queasy.char2 == dynarate_list_rcode) & (Queasy.number1 == zimkateg.zikatnr) & (Queasy.deci1 == dynarate_list_w_day)).order_by(Queasy._recid).all():
                    queasy.deci2 =  to_decimal(curr_counter)
            else:
                return

    fill_dynarate_counter()

    return generate_output()