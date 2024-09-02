from functions.additional_functions import *
import decimal
from models import Bk_setup

def prepare_basetup_adminbl():
    t_bk_setup_list = []
    bk_setup = None

    t_bk_setup = None

    t_bk_setup_list, T_bk_setup = create_model_like(Bk_setup, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bk_setup_list, bk_setup


        nonlocal t_bk_setup
        nonlocal t_bk_setup_list
        return {"t-bk-setup": t_bk_setup_list}

    for bk_setup in db_session.query(Bk_setup).all():
        t_bk_setup = T_bk_setup()
        t_bk_setup_list.append(t_bk_setup)

        buffer_copy(bk_setup, t_bk_setup)
        t_bk_setup.rec_id = bk_setup._recid

    return generate_output()