from functions.additional_functions import *
import decimal
from models import Counters

def next_counterbl(counterno:int):
    t_counters_list = []
    counters = None

    t_counters = None

    t_counters_list, T_counters = create_model_like(Counters)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_counters_list, counters


        nonlocal t_counters
        nonlocal t_counters_list
        return {"t-counters": t_counters_list}

    counters = db_session.query(Counters).filter(
            (Counters.counter_no == counterno)).first()

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = counterno
        counters.counter_bez = to_string(counterno)
        counters.counter = 0


    counters.counter = counters.counter + 1

    counters = db_session.query(Counters).first()
    t_counters = T_counters()
    t_counters_list.append(t_counters)

    buffer_copy(counters, t_counters)

    return generate_output()