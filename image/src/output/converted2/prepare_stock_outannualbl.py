#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import L_hauptgrp

def prepare_stock_outannualbl():

    prepare_cache ([L_hauptgrp])

    ci_date = None
    t_l_hauptgrp_list = []
    l_hauptgrp = None

    t_l_hauptgrp = None

    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, t_l_hauptgrp_list, l_hauptgrp


        nonlocal t_l_hauptgrp
        nonlocal t_l_hauptgrp_list

        return {"ci_date": ci_date, "t-l-hauptgrp": t_l_hauptgrp_list}


    ci_date = get_output(htpdate(87))

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        t_l_hauptgrp.endkum = l_hauptgrp.endkum
        t_l_hauptgrp.bezeich = l_hauptgrp.bezeich

    return generate_output()