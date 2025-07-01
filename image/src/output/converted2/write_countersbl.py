#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Counters

t_counters_list, T_counters = create_model_like(Counters)

def write_countersbl(case_type:int, counter_no:int, t_counters_list:[T_counters]):

    prepare_cache ([Counters])

    success_flag = False
    counters = None

    t_counters = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, counters
        nonlocal case_type, counter_no


        nonlocal t_counters

        return {"success_flag": success_flag}

    t_counters = query(t_counters_list, first=True)

    if not t_counters:

        return generate_output()

    if case_type == 1:

        counters = get_cache (Counters, {"counter_no": [(eq, counter_no)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)

            buffer_copy(t_counters, counters)
            success_flag = True
        counters.counter = counters.counter + 1


        pass
        success_flag = True

    return generate_output()