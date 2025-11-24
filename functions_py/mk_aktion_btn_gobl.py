#using conversion tools version: 1.0.0.119
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Akthdr, Counters
from functions.next_counter_for_update import next_counter_for_update

t_akthdr_data, T_akthdr = create_model_like(Akthdr)

def mk_aktion_btn_gobl(t_akthdr_data:[T_akthdr]):

    prepare_cache ([Akthdr, Counters])

    curr_counter = 0
    akthdr = counters = None

    t_akthdr = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""

    def generate_output():
        nonlocal curr_counter, akthdr, counters


        nonlocal t_akthdr

        return {"curr_counter": curr_counter}

    counters = get_cache (Counters, {"counter_no": [(eq, 26)]})

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 26
        counters.counter_bez = "Counter for sales activity"
    # counters.counter = counters.counter + 1

    last_count, error_lock = get_output(next_counter_for_update(26))

    # curr_counter = counters.counter
    curr_counter = last_count

    pass

    t_akthdr = query(t_akthdr_data, first=True)
    akthdr = Akthdr()
    db_session.add(akthdr)

    buffer_copy(t_akthdr, akthdr)
    # akthdr.aktnr = counters.counter
    akthdr.aktnr = curr_counter

    return generate_output()