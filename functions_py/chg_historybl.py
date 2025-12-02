#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import History

t_history_data, T_history = create_model_like(History)

def chg_historybl(s_recid:int, t_history_data:[T_history]):
    successflag = False
    history = None

    t_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, history
        nonlocal s_recid


        nonlocal t_history

        return {"successflag": successflag}

    t_history = query(t_history_data, first=True)

    if not t_history:

        return generate_output()

    # history = get_cache (History, {"_recid": [(eq, s_recid)]})
    history = db_session.query(History).filter(History._recid == s_recid).with_for_update().first()

    if history:
        buffer_copy(t_history, history)
        pass
        successflag = True

    return generate_output()
