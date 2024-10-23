from functions.additional_functions import *
import decimal
from models import Queasy

t_queasy_list, T_queasy = create_model_like(Queasy)

def create_queasybl(t_queasy_list:[T_queasy]):
    q_recid = 0
    queasy = None

    t_queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q_recid, queasy


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"q_recid": q_recid}

    t_queasy = query(t_queasy_list, first=True)

    if t_queasy:
        queasy = Queasy()
        db_session.add(queasy)

        buffer_copy(t_queasy, queasy)
        q_recid = queasy._recid

    return generate_output()