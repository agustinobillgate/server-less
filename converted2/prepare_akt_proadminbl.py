#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_code

def prepare_akt_proadminbl():
    t_akt_code_data = []
    akt_code = None

    t_akt_code = None

    t_akt_code_data, T_akt_code = create_model_like(Akt_code, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_akt_code_data, akt_code


        nonlocal t_akt_code
        nonlocal t_akt_code_data

        return {"t-akt-code": t_akt_code_data}

    for akt_code in db_session.query(Akt_code).order_by(Akt_code.aktionscode).all():
        t_akt_code = T_akt_code()
        t_akt_code_data.append(t_akt_code)

        buffer_copy(akt_code, t_akt_code)
        t_akt_code.rec_id = akt_code._recid

    return generate_output()