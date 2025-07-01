#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_code

def prepare_aktcode_adminbl():
    t_akt_code_list = []
    akt_code = None

    t_akt_code = None

    t_akt_code_list, T_akt_code = create_model_like(Akt_code, {"recid_akt_code":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_akt_code_list, akt_code


        nonlocal t_akt_code
        nonlocal t_akt_code_list

        return {"t-akt-code": t_akt_code_list}

    for akt_code in db_session.query(Akt_code).filter(
             (Akt_code.aktiongrup == 1)).order_by(Akt_code.aktionscode).all():
        t_akt_code = T_akt_code()
        t_akt_code_list.append(t_akt_code)

        buffer_copy(akt_code, t_akt_code)
        t_akt_code.recid_akt_code = akt_code._recid

    return generate_output()