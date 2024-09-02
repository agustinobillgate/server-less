from functions.additional_functions import *
import decimal
from models import Queasy

def cash_flowbl():
    t_cflow_list = []
    queasy = None

    t_cflow = None

    t_cflow_list, T_cflow = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_cflow_list, queasy


        nonlocal t_cflow
        nonlocal t_cflow_list
        return {"t-cflow": t_cflow_list}

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 177)).all():
        t_cflow = T_cflow()
        t_cflow_list.append(t_cflow)

        buffer_copy(queasy, t_cflow)

        if queasy.number1 != 0:
            t_cflow.deci1 = queasy.number1

    return generate_output()