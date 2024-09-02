from functions.additional_functions import *
import decimal
from models import Zimkateg, Queasy

def prepare_rmcat_adminbl():
    t_zimkateg_list = []
    t_queasy_list = []
    zimkateg = queasy = None

    t_zimkateg = t_queasy = None

    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)
    t_queasy_list, T_queasy = create_model_like(Queasy)


    db_session = local_storage.db_session
    result = db_session.execute(sa.text("SELECT current_schema();"))
    current_schema = result.scalar()
    print("Current Schema:", current_schema)

    def generate_output():
        nonlocal t_zimkateg_list, t_queasy_list, zimkateg, queasy


        nonlocal t_zimkateg, t_queasy
        nonlocal t_zimkateg_list, t_queasy_list
        return {"t-zimkateg": t_zimkateg_list, "t-queasy": t_queasy_list}


    for zimkateg in db_session.query(Zimkateg).all():
        t_zimkateg = T_zimkateg()
        t_zimkateg_list.append(t_zimkateg)
        buffer_copy(zimkateg, t_zimkateg)

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 152)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    return generate_output()