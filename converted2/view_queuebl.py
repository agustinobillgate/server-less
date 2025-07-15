#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Zimmer

def view_queuebl():

    prepare_cache ([Zimmer])

    t_queasy_data = []
    queasy = zimmer = None

    t_queasy = None

    t_queasy_data, T_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_data, queasy, zimmer


        nonlocal t_queasy
        nonlocal t_queasy_data

        return {"t-queasy": t_queasy_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 162)).order_by(Queasy.char1).all():

        zimmer = get_cache (Zimmer, {"zinr": [(eq, queasy.char1)]})

        if zimmer and zimmer.zistatus < 3:
            t_queasy = T_queasy()
            t_queasy_data.append(t_queasy)

            buffer_copy(queasy, t_queasy)

    return generate_output()