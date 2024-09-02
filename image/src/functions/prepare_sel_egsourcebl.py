from functions.additional_functions import *
import decimal
from models import Queasy

def prepare_sel_egsourcebl():
    t_queasy_list = []
    queasy = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model("T_queasy", {"number1":int, "char1":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_queasy_list, queasy


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"t-queasy": t_queasy_list}

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 130)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        t_queasy.number1 = queasy.number1
        t_queasy.char1 = queasy.char1

    return generate_output()