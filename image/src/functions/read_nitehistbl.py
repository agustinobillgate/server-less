from functions.additional_functions import *
import decimal
from datetime import date
from models import Nitehist

def read_nitehistbl(case_type:int, int1:int, int2:int, date1:date, char1:str):
    t_nitehist_list = []
    nitehist = None

    t_nitehist = None

    t_nitehist_list, T_nitehist = create_model_like(Nitehist)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_nitehist_list, nitehist


        nonlocal t_nitehist
        nonlocal t_nitehist_list
        return {"t-nitehist": t_nitehist_list}

    if case_type == 1:

        nitehist = db_session.query(Nitehist).filter(
                (Nitehist.datum == date1)).first()

        if nitehist:
            t_nitehist = T_nitehist()
            t_nitehist_list.append(t_nitehist)

            buffer_copy(nitehist, t_nitehist)
    elif case_type == 2:

        for nitehist in db_session.query(Nitehist).filter(
                (Nitehist.datum == date1) &  (Nitehist.reihenfolge == int1)).all():
            t_nitehist = T_nitehist()
            t_nitehist_list.append(t_nitehist)

            buffer_copy(nitehist, t_nitehist)

    return generate_output()