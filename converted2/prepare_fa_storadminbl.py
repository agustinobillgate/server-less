#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fa_lager

def prepare_fa_storadminbl():
    t_fa_lager_data = []
    fa_lager = None

    t_fa_lager = None

    t_fa_lager_data, T_fa_lager = create_model_like(Fa_lager, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_fa_lager_data, fa_lager


        nonlocal t_fa_lager
        nonlocal t_fa_lager_data

        return {"t-fa-lager": t_fa_lager_data}

    for fa_lager in db_session.query(Fa_lager).order_by(Fa_lager._recid).all():
        t_fa_lager = T_fa_lager()
        t_fa_lager_data.append(t_fa_lager)

        buffer_copy(fa_lager, t_fa_lager)
        t_fa_lager.rec_id = fa_lager._recid

    return generate_output()