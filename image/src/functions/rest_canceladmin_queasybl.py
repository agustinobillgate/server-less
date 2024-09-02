from functions.additional_functions import *
import decimal
from models import Queasy

def rest_canceladmin_queasybl():
    t_queasy_list = []
    queasy = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"t-queasy": t_queasy_list}

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 11)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    return generate_output()