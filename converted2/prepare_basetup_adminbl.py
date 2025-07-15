#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_setup

def prepare_basetup_adminbl():
    t_bk_setup_data = []
    bk_setup = None

    t_bk_setup = None

    t_bk_setup_data, T_bk_setup = create_model_like(Bk_setup, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bk_setup_data, bk_setup


        nonlocal t_bk_setup
        nonlocal t_bk_setup_data

        return {"t-bk-setup": t_bk_setup_data}

    for bk_setup in db_session.query(Bk_setup).order_by(Bk_setup.setup_id).all():
        t_bk_setup = T_bk_setup()
        t_bk_setup_data.append(t_bk_setup)

        buffer_copy(bk_setup, t_bk_setup)
        t_bk_setup.rec_id = bk_setup._recid

    return generate_output()