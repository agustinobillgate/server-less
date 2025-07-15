#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpgen

def prepare_rmaingrp_adminbl():
    t_wgrpgen_data = []
    wgrpgen = None

    t_wgrpgen = None

    t_wgrpgen_data, T_wgrpgen = create_model_like(Wgrpgen)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_wgrpgen_data, wgrpgen


        nonlocal t_wgrpgen
        nonlocal t_wgrpgen_data

        return {"t-wgrpgen": t_wgrpgen_data}

    for wgrpgen in db_session.query(Wgrpgen).order_by(Wgrpgen.eknr).all():
        t_wgrpgen = T_wgrpgen()
        t_wgrpgen_data.append(t_wgrpgen)

        buffer_copy(wgrpgen, t_wgrpgen)

    return generate_output()