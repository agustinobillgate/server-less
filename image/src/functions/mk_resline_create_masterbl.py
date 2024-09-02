from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Master, Bediener, Counters, Res_history

def mk_resline_create_masterbl(resnr:int, gastnr:int, invno_flag:bool, user_init:str):
    gastnrpay = 0
    t_master_list = []
    master = bediener = counters = res_history = None

    t_master = None

    t_master_list, T_master = create_model_like(Master)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gastnrpay, t_master_list, master, bediener, counters, res_history


        nonlocal t_master
        nonlocal t_master_list
        return {"gastnrpay": gastnrpay, "t-master": t_master_list}

    def create_master():

        nonlocal gastnrpay, t_master_list, master, bediener, counters, res_history


        nonlocal t_master
        nonlocal t_master_list


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


        pass

        if invno_flag:

            counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 3)).first()
            counters.counter = counters.counter + 1

            counters = db_session.query(Counters).first()
            master.rechnr = counters.counter

        master = db_session.query(Master).first()
        t_master = T_master()
        t_master_list.append(t_master)

        buffer_copy(master, t_master)
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "MASTER BILL"
        res_history.aenderung = "Create Master Bill, ResNo  ==  " + to_string(resnr) +\
                " Master BillNo  ==  " + to_string(master.rechnr)

        res_history = db_session.query(Res_history).first()


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    create_master()

    return generate_output()