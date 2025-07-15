#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_history

t_res_history_data, T_res_history = create_model_like(Res_history)

def chg_prcode_create_logbl(t_res_history_data:[T_res_history]):
    res_history = None

    t_res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_history


        nonlocal t_res_history

        return {}

    for t_res_history in query(t_res_history_data):
        res_history = Res_history()
        db_session.add(res_history)

        buffer_copy(t_res_history, res_history)

    return generate_output()