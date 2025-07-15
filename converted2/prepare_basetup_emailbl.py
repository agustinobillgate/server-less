#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def prepare_basetup_emailbl():
    q_list_data = []
    queasy = None

    q_list = None

    q_list_data, Q_list = create_model_like(Queasy, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q_list_data, queasy


        nonlocal q_list
        nonlocal q_list_data

        return {"q-list": q_list_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 138)).order_by(Queasy.number1).all():
        q_list = Q_list()
        q_list_data.append(q_list)

        buffer_copy(queasy, q_list)
        q_list.rec_id = queasy._recid

    return generate_output()