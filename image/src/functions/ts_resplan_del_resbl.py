from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy

def ts_resplan_del_resbl(curr_dept:int, curr_date:date, rec_id:int, user_init:str):
    t_queasy33_list = []
    queasy = None

    t_queasy33 = qsy = None

    t_queasy33_list, T_queasy33 = create_model_like(Queasy, {"rec_id":int})

    Qsy = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy33_list, queasy
        nonlocal qsy


        nonlocal t_queasy33, qsy
        nonlocal t_queasy33_list
        return {"t-queasy33": t_queasy33_list}

    def del_res():

        nonlocal t_queasy33_list, queasy
        nonlocal qsy


        nonlocal t_queasy33, qsy
        nonlocal t_queasy33_list


        Qsy = Queasy

        qsy = db_session.query(Qsy).filter(
                    (Qsy._recid == rec_id)).first()
        qsy.logi3 = False
        qsy.date3 = get_current_date()
        qsy.deci3 = get_current_time_in_seconds()
        qsy.char3 = qsy.char3 + user_init + ";"
        qsy.betriebsnr = 2

        qsy = db_session.query(Qsy).first()


    del_res()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 33) &  (Queasy.number1 == curr_dept) &  (Queasy.date1 == curr_date) &  (Queasy.logi2 == False) &  (Queasy.logi3) &  (Queasy.betriebsnr == 0)).all():
        t_queasy33 = T_queasy33()
        t_queasy33_list.append(t_queasy33)

        buffer_copy(queasy, t_queasy33)
        t_queasy33.rec_id = queasy._recid

    return generate_output()