from functions.additional_functions import *
import decimal
from models import Nightaudit

def read_nightauditbl(case_type:int, int1:int, int2:int, char1:str, log1:bool):
    t_nightaudit_list = []
    nightaudit = None

    t_nightaudit = None

    t_nightaudit_list, T_nightaudit = create_model_like(Nightaudit, {"n_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nightaudit_list, nightaudit


        nonlocal t_nightaudit
        nonlocal t_nightaudit_list
        return {"t-nightaudit": t_nightaudit_list}

    if case_type == 1:

        for nightaudit in db_session.query(Nightaudit).filter(
                (abschlussart) &  (selektion)).all():
            t_nightaudit = T_nightaudit()
            t_nightaudit_list.append(t_nightaudit)

            buffer_copy(nightaudit, t_nightaudit)
            t_nightaudit.n_recid = nightaudit._recid


    elif case_type == 2:

        for nightaudit in db_session.query(Nightaudit).all():
            t_nightaudit = T_nightaudit()
            t_nightaudit_list.append(t_nightaudit)

            buffer_copy(nightaudit, t_nightaudit)
            t_nightaudit.n_recid = nightaudit._recid

    return generate_output()