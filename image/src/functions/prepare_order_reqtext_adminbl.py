from functions.additional_functions import *
import decimal
from models import Queasy

def prepare_order_reqtext_adminbl():
    t_queasy_list = []
    queasy = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model("T_queasy", {"char1":str, "number1":int, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"t-queasy": t_queasy_list}

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 12)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        t_queasy.char1 = queasy.char1
        t_queasy.number1 = queasy.number1
        t_queasy.rec_id = queasy._recid

    return generate_output()