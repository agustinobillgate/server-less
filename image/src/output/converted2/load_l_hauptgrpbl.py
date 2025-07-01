#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_hauptgrp

def load_l_hauptgrpbl():
    t_l_hauptgrp_list = []
    l_hauptgrp = None

    t_l_hauptgrp = None

    t_l_hauptgrp_list, T_l_hauptgrp = create_model_like(L_hauptgrp)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_hauptgrp_list, l_hauptgrp


        nonlocal t_l_hauptgrp
        nonlocal t_l_hauptgrp_list

        return {"t-l-hauptgrp": t_l_hauptgrp_list}

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        buffer_copy(l_hauptgrp, t_l_hauptgrp)

    return generate_output()