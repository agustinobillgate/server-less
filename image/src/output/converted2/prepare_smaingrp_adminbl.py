#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_hauptgrp

def prepare_smaingrp_adminbl():

    prepare_cache ([L_hauptgrp])

    t_l_hauptgrp_list = []
    l_hauptgrp = None

    t_l_hauptgrp = None

    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_hauptgrp_list, l_hauptgrp


        nonlocal t_l_hauptgrp
        nonlocal t_l_hauptgrp_list

        return {"t-l-hauptgrp": t_l_hauptgrp_list}

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        t_l_hauptgrp.endkum = l_hauptgrp.endkum
        t_l_hauptgrp.bezeich = l_hauptgrp.bezeich

    return generate_output()