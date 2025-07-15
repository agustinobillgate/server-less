#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Counters

def next_counterbl(counterno:int):
    t_counters_data = []
    counters = None

    t_counters = None

    t_counters_data, T_counters = create_model_like(Counters)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_counters_data, counters
        nonlocal counterno


        nonlocal t_counters
        nonlocal t_counters_data

        return {"t-counters": t_counters_data}

    counters = get_cache (Counters, {"counter_no": [(eq, counterno)]})

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = counterno
        counters.counter_bez = to_string(counterno)
        counters.counter = 0


    counters.counter = counters.counter + 1


    pass
    t_counters = T_counters()
    t_counters_data.append(t_counters)

    buffer_copy(counters, t_counters)

    return generate_output()