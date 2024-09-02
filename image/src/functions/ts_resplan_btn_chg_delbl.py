from functions.additional_functions import *
import decimal
from models import Queasy

def ts_resplan_btn_chg_delbl(s_recid:int):
    t_queasy_list = []
    queasy = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model("T_queasy", {"char1":str, "char2":str, "number3":int, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"t-queasy": t_queasy_list}

    queasy = db_session.query(Queasy).filter(
            (Queasy._recid == s_recid)).first()
    t_queasy = T_queasy()
    t_queasy_list.append(t_queasy)

    t_queasy.char1 = queasy.char1
    t_queasy.char2 = queasy.char2
    t_queasy.number3 = queasy.number3
    t_queasy.rec_id = queasy._recid

    return generate_output()