from functions.additional_functions import *
import decimal
from models import History

def chg_historybl(s_recid:int, t_history:[T_history]):
    successflag = False
    history = None

    t_history = None

    t_history_list, T_history = create_model_like(History)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, history


        nonlocal t_history
        nonlocal t_history_list
        return {"successflag": successflag}

    t_history = query(t_history_list, first=True)

    if not t_history:

        return generate_output()

    history = db_session.query(History).filter(
            (History._recid == s_recid)).first()

    if history:
        buffer_copy(t_history, history)

        history = db_session.query(History).first()
        successflag = True

    return generate_output()