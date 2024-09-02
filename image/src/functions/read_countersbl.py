from functions.additional_functions import *
import decimal
from models import Counters

def read_countersbl(case_type:int, counterno:int):
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

    if case_type == 1:

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == counterno)).first()

        if counters:
            t_counters = T_counters()
            t_counters_list.append(t_counters)

            buffer_copy(counters, t_counters)
    elif case_type == 2:

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == counterno)).first()
        counters.counter = counters.counter + 1

        counters = db_session.query(Counters).first()
        t_counters = T_counters()
        t_counters_list.append(t_counters)

        buffer_copy(counters, t_counters)

    return generate_output()