#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_kateg

def prepare_fa_kategadminbl():
    t_fa_kateg_data = []
    fa_kateg = None

    t_fa_kateg = None

    t_fa_kateg_data, T_fa_kateg = create_model_like(Fa_kateg, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_fa_kateg_data, fa_kateg


        nonlocal t_fa_kateg
        nonlocal t_fa_kateg_data

        return {"t-fa-kateg": t_fa_kateg_data}

    for fa_kateg in db_session.query(Fa_kateg).order_by(Fa_kateg.katnr).all():
        t_fa_kateg = T_fa_kateg()
        t_fa_kateg_data.append(t_fa_kateg)

        buffer_copy(fa_kateg, t_fa_kateg)
        t_fa_kateg.rec_id = fa_kateg._recid

    return generate_output()