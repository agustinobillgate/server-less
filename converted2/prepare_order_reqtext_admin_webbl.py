#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def prepare_order_reqtext_admin_webbl():

    prepare_cache ([Queasy])

    t_queasy_data = []
    queasy = None

    t_queasy = None

    t_queasy_data, T_queasy = create_model("T_queasy", {"char1":string, "number1":int, "number2":int, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_data, queasy


        nonlocal t_queasy
        nonlocal t_queasy_data

        return {"t-queasy": t_queasy_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 12)).order_by(Queasy.number1).all():
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        t_queasy.char1 = queasy.char1
        t_queasy.number1 = queasy.number1
        t_queasy.number2 = queasy.number2
        t_queasy.rec_id = queasy._recid

    return generate_output()