#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def cash_flowbl():
    t_cflow_data = []
    queasy = None

    t_cflow = None

    t_cflow_data, T_cflow = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_cflow_data, queasy


        nonlocal t_cflow
        nonlocal t_cflow_data

        return {"t-cflow": t_cflow_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 177)).order_by(Queasy._recid).all():
        t_cflow = T_cflow()
        t_cflow_data.append(t_cflow)

        buffer_copy(queasy, t_cflow)

        if queasy.number1 != 0:
            t_cflow.deci1 =  to_decimal(queasy.number1)

    return generate_output()