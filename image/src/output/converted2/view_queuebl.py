#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Zimmer

def view_queuebl():

    prepare_cache ([Zimmer])

    t_queasy_list = []
    queasy = zimmer = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy, zimmer


        nonlocal t_queasy
        nonlocal t_queasy_list

        return {"t-queasy": t_queasy_list}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 162)).order_by(Queasy.char1).all():

        zimmer = get_cache (Zimmer, {"zinr": [(eq, queasy.char1)]})

        if zimmer and zimmer.zistatus < 3:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)

    return generate_output()