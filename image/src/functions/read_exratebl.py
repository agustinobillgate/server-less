from functions.additional_functions import *
import decimal
from datetime import date
from models import Exrate

def read_exratebl(case_type:int, artno:int, datum:date):
    t_exrate_list = []
    exrate = None

    t_exrate = None

    t_exrate_list, T_exrate = create_model_like(Exrate)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_exrate_list, exrate


        nonlocal t_exrate
        nonlocal t_exrate_list
        return {"t-exrate": t_exrate_list}

    if case_type == 1:

        exrate = db_session.query(Exrate).filter(
                (Exrate.artnr == artno) &  (Exrate.datum == datum)).first()

        if exrate:
            t_exrate = T_exrate()
            t_exrate_list.append(t_exrate)

            buffer_copy(exrate, t_exrate)

    return generate_output()