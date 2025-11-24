#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Counters
from functions.next_counter_for_update import next_counter_for_update

def read_countersbl(case_type:int, counterno:int):
    t_counters_data = []
    counters = None

    t_counters = None

    t_counters_data, T_counters = create_model_like(Counters)

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    
    def generate_output():
        nonlocal t_counters_data, counters
        nonlocal case_type, counterno


        nonlocal t_counters
        nonlocal t_counters_data

        return {"t-counters": t_counters_data}

    if case_type == 1:

        counters = get_cache (Counters, {"counter_no": [(eq, counterno)]})

        if counters:
            t_counters = T_counters()
            t_counters_data.append(t_counters)

            buffer_copy(counters, t_counters)
    elif case_type == 2:

        # counters = get_cache (Counters, {"counter_no": [(eq, counterno)]})
        # counters.counter = counters.counter + 1
        last_count, error_lock = next_counter_for_update(counterno, last_count, error_lock)
        counters = get_cache (Counters, {"counter_no": [(eq, counterno)]})


        pass
        t_counters = T_counters()
        t_counters_data.append(t_counters)

        buffer_copy(counters, t_counters)

    return generate_output()