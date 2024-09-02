from functions.additional_functions import *
import decimal
from models import Queasy, Zimmer

def view_queuebl():
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
            (Queasy.key == 162)).all():

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == queasy.char1)).first()

        if zimmer and zimmer.zistatus < 3:
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)

    return generate_output()