from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Tisch

def ts_resplan_disp_resdatabl(case_type:int, von_tisch:int, curr_dept:int, curr_date:date):
    pax = 0
    t_queasy33_list = []
    queasy = tisch = None

    t_queasy33 = None

    t_queasy33_list, T_queasy33 = create_model_like(Queasy, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pax, t_queasy33_list, queasy, tisch


        nonlocal t_queasy33
        nonlocal t_queasy33_list
        return {"pax": pax, "t-queasy33": t_queasy33_list}

    if case_type == 1:

        tisch = db_session.query(Tisch).filter(
                (Tischnr == von_tisch)).first()
        pax = tisch.normalbeleg

    elif case_type == 2:

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 33) &  (Queasy.number1 == curr_dept) &  (Queasy.date1 == curr_date) &  (Queasy.logi2 == False) &  (Queasy.logi3) &  (Queasy.betriebsnr == 0)).all():
            t_queasy33 = T_queasy33()
            t_queasy33_list.append(t_queasy33)

            buffer_copy(queasy, t_queasy33)
            t_queasy33.rec_id = queasy._recid

    return generate_output()