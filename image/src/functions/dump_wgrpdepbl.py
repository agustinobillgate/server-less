from functions.additional_functions import *
import decimal
from models import Wgrpdep

def dump_wgrpdepbl():
    t_wgrpdep_list = []
    wgrpdep = None

    t_wgrpdep = None

    t_wgrpdep_list, T_wgrpdep = create_model_like(Wgrpdep)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_wgrpdep_list, wgrpdep


        nonlocal t_wgrpdep
        nonlocal t_wgrpdep_list
        return {"t-wgrpdep": t_wgrpdep_list}

    for wgrpdep in db_session.query(Wgrpdep).all():
        t_wgrpdep = T_wgrpdep()
        t_wgrpdep_list.append(t_wgrpdep)

        buffer_copy(wgrpdep, t_wgrpdep)

    return generate_output()