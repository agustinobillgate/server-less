from functions.additional_functions import *
import decimal
from models import Counters

def write_countersbl(case_type:int, counter_no:int, t_counters:[T_counters]):
    success_flag = False
    counters = None

    t_counters = None

    t_counters_list, T_counters = create_model_like(Counters)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, counters


        nonlocal t_counters
        nonlocal t_counters_list
        return {"success_flag": success_flag}

    t_counters = query(t_counters_list, first=True)

    if not t_counters:

        return generate_output()

    if case_type == 1:

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == counter_no)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            buffer_copy(t_counters, counters)
            success_flag = True
        counters.counter = counters.counter + 1

        counters = db_session.query(Counters).first()
        success_flag = True

    return generate_output()