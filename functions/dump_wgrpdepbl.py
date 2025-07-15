#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpdep

def dump_wgrpdepbl():
    t_wgrpdep_data = []
    wgrpdep = None

    t_wgrpdep = None

    t_wgrpdep_data, T_wgrpdep = create_model_like(Wgrpdep)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_wgrpdep_data, wgrpdep


        nonlocal t_wgrpdep
        nonlocal t_wgrpdep_data

        return {"t-wgrpdep": t_wgrpdep_data}

    for wgrpdep in db_session.query(Wgrpdep).order_by(Wgrpdep._recid).all():
        t_wgrpdep = T_wgrpdep()
        t_wgrpdep_data.append(t_wgrpdep)

        buffer_copy(wgrpdep, t_wgrpdep)

    return generate_output()