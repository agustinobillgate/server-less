from functions.additional_functions import *
import decimal
from models import History

def view_historybl(resnr:int, hist1:[Hist1]):
    t_history_list = []
    history = None

    t_history = hist1 = None

    t_history_list, T_history = create_model_like(History)
    hist1_list, Hist1 = create_model_like(History)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_history_list, history


        nonlocal t_history, hist1
        nonlocal t_history_list, hist1_list
        return {"t-history": t_history_list}


    hist1 = query(hist1_list, first=True)

    for history in db_session.query(History).filter(
            (History.resnr == resnr) &  (((History.ankunft - hist1.ankunft) <= 30) |  ((hist1.ankunft - History.ankunft) <= 30))).all():
        t_history = T_history()
        t_history_list.append(t_history)

        buffer_copy(history, t_history)

    return generate_output()