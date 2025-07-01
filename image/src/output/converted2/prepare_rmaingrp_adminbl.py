#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpgen

def prepare_rmaingrp_adminbl():
    t_wgrpgen_list = []
    wgrpgen = None

    t_wgrpgen = None

    t_wgrpgen_list, T_wgrpgen = create_model_like(Wgrpgen)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_wgrpgen_list, wgrpgen


        nonlocal t_wgrpgen
        nonlocal t_wgrpgen_list

        return {"t-wgrpgen": t_wgrpgen_list}

    for wgrpgen in db_session.query(Wgrpgen).order_by(Wgrpgen.eknr).all():
        t_wgrpgen = T_wgrpgen()
        t_wgrpgen_list.append(t_wgrpgen)

        buffer_copy(wgrpgen, t_wgrpgen)

    return generate_output()