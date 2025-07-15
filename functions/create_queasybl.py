#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

t_queasy_data, T_queasy = create_model_like(Queasy)

def create_queasybl(t_queasy_data:[T_queasy]):

    prepare_cache ([Queasy])

    q_recid = 0
    queasy = None

    t_queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q_recid, queasy


        nonlocal t_queasy

        return {"q_recid": q_recid}

    t_queasy = query(t_queasy_data, first=True)

    if t_queasy:
        queasy = Queasy()
        db_session.add(queasy)

        buffer_copy(t_queasy, queasy)
        pass
        q_recid = queasy._recid

    return generate_output()