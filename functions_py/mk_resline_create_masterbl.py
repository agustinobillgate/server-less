#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Master, Bediener, Counters, Res_history
from functions.next_counter_for_update import next_counter_for_update

def mk_resline_create_masterbl(resnr:int, gastnr:int, invno_flag:bool, user_init:string):

    prepare_cache ([Bediener, Counters, Res_history])

    gastnrpay = 0
    t_master_data = []
    master = bediener = counters = res_history = None

    t_master = None

    t_master_data, T_master = create_model_like(Master)

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    user_init = user_init.strip()

    def generate_output():
        nonlocal gastnrpay, t_master_data, master, bediener, counters, res_history
        nonlocal resnr, gastnr, invno_flag, user_init

        nonlocal t_master
        nonlocal t_master_data

        return {"gastnrpay": gastnrpay, "t-master": t_master_data}

    def create_master():

        nonlocal gastnrpay, t_master_data, master, bediener, counters, res_history
        nonlocal resnr, gastnr, invno_flag, user_init


        nonlocal t_master
        nonlocal t_master_data


        master = Master()
        db_session.add(master)

        master.resnr = resnr
        master.gastnr = gastnr
        master.gastnrpay = gastnr
        master.active = True
        master.rechnrstart = 1
        master.rechnrend = 1
        master.umsatzart[0] = True
        master.umsatzart[1] = True
        gastnrpay = gastnr


        if invno_flag:

            # counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
            # counters.counter = counters.counter + 1
            last_count, error_lock = get_output(next_counter_for_update(3))

            pass
            # master.rechnr = counters.counter
            master.rechnr = last_count


        pass
        t_master = T_master()
        t_master_data.append(t_master)

        buffer_copy(master, t_master)
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "MASTER BILL"
        res_history.aenderung = "Create Master Bill, ResNo = " + to_string(resnr) +\
                " Master BillNo = " + to_string(master.rechnr)


        pass
        pass


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    create_master()

    return generate_output()