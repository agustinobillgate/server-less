#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import History

t_history_list, T_history = create_model_like(History)

def chg_historybl(s_recid:int, t_history_list:[T_history]):
    successflag = False
    history = None

    t_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, history
        nonlocal s_recid


        nonlocal t_history

        return {"successflag": successflag}

    t_history = query(t_history_list, first=True)

    if not t_history:

        return generate_output()

    history = get_cache (History, {"_recid": [(eq, s_recid)]})

    if history:
        buffer_copy(t_history, history)
        pass
        successflag = True

    return generate_output()