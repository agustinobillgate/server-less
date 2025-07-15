from functions.additional_functions import *
import decimal
from models import Akthdr, Counters

t_akthdr_list, T_akthdr = create_model_like(Akthdr)

def mk_aktion_btn_gobl(t_akthdr_list:[T_akthdr]):
    curr_counter = 0
    akthdr = counters = None

    t_akthdr = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_counter, akthdr, counters


        nonlocal t_akthdr
        nonlocal t_akthdr_list
        return {"curr_counter": curr_counter}

    counters = db_session.query(Counters).filter(
             (Counters.counter_no == 26)).first()

    if not counters:
        counters = Counters()
        db_session.add(counters)

        counters.counter_no = 26
        counters.counter_bez = "Counter for sales activity"
    counters.counter = counters.counter + 1
    curr_counter = counters.counter

    t_akthdr = query(t_akthdr_list, first=True)
    akthdr = Akthdr()
    db_session.add(akthdr)

    buffer_copy(t_akthdr, akthdr)
    akthdr.aktnr = counters.counter

    return generate_output()