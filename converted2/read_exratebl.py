#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Exrate

def read_exratebl(case_type:int, artno:int, datum:date):
    t_exrate_data = []
    exrate = None

    t_exrate = None

    t_exrate_data, T_exrate = create_model_like(Exrate)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_exrate_data, exrate
        nonlocal case_type, artno, datum


        nonlocal t_exrate
        nonlocal t_exrate_data

        return {"t-exrate": t_exrate_data}

    if case_type == 1:

        exrate = get_cache (Exrate, {"artnr": [(eq, artno)],"datum": [(eq, datum)]})

        if exrate:
            t_exrate = T_exrate()
            t_exrate_data.append(t_exrate)

            buffer_copy(exrate, t_exrate)

    return generate_output()