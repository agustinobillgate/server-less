from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from models import History

def read_historybl(case_type:int, gastno:int, resno:int, reslinno:int, rmno:str, arrive:date, depart:date):
    t_history_list = []
    ind_gastnr:int = 0
    wig_gastnr:int = 0
    i_anzahl:int = 0
    history = None

    t_history = None

    t_history_list, T_history = create_model_like(History)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_history_list, ind_gastnr, wig_gastnr, i_anzahl, history


        nonlocal t_history
        nonlocal t_history_list
        return {"t-history": t_history_list}

    if case_type == 1:

        history = db_session.query(History).filter(
                (History.gastnr == gastno) &  (History.resnr == resno) &  (History.reslinnr == reslinno)).first()

        if history:
            t_history = T_history()
            t_history_list.append(t_history)

            buffer_copy(history, t_history)
    elif case_type == 2:
        wig_gastnr = get_output(htpint(109))
        ind_gastnr = get_output(htpint(123))

        for history in db_session.query(History).filter(
                (History.gastnr == gastno)).all():
            t_history = T_history()
            t_history_list.append(t_history)

            buffer_copy(history, t_history)

            if gastno == wig_gastnr or gastno == ind_gastnr:
                i_anzahl = i_anzahl + 1

            if i_anzahl == 4:

                return generate_output()
    elif case_type == 3:

        history = db_session.query(History).filter(
                (History._recid == gastno)).first()

        if history:
            t_history = T_history()
            t_history_list.append(t_history)

            buffer_copy(history, t_history)
    elif case_type == 4:

        history = db_session.query(History).filter(
                (History.resnr == resno) &  (History.reslinnr == reslinno) &  (num_entries(History.bemerk, ": == ") >= 2) &  (trim(entry(1, History.bemerk, ": == ")) == " == " + trim(rmno))).first()

        if history:
            t_history = T_history()
            t_history_list.append(t_history)

            buffer_copy(history, t_history)
    elif case_type == 5:

        for history in db_session.query(History).filter(
                (History.gastnr == gastno) &  (History.abreise <= TODAY)).all():
            t_history = T_history()
            t_history_list.append(t_history)

            buffer_copy(history, t_history)
    elif case_type == 6:

        history = db_session.query(History).filter(
                (History.resnr == resno) &  (History.reslinnr == reslinno) &  (History.zi_wechsel == False)).first()

        if history:
            t_history = T_history()
            t_history_list.append(t_history)

            buffer_copy(history, t_history)
    elif case_type == 7:

        history = db_session.query(History).filter(
                (History.resnr == resno) &  (History.reslinnr == reslinno)).first()

        if history:
            t_history = T_history()
            t_history_list.append(t_history)

            buffer_copy(history, t_history)

    return generate_output()