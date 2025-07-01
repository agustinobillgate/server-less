#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_hauptgrp, L_lager, Htparam

def prepare_mat_reconsilehisbl():

    prepare_cache ([Htparam])

    from_grp = 0
    to_date = None
    from_date = None
    long_digit = False
    t_l_hauptgrp_list = []
    t_l_lager_list = []
    l_hauptgrp = l_lager = htparam = None

    t_l_hauptgrp = t_l_lager = None

    t_l_hauptgrp_list, T_l_hauptgrp = create_model_like(L_hauptgrp)
    t_l_lager_list, T_l_lager = create_model_like(L_lager)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_grp, to_date, from_date, long_digit, t_l_hauptgrp_list, t_l_lager_list, l_hauptgrp, l_lager, htparam


        nonlocal t_l_hauptgrp, t_l_lager
        nonlocal t_l_hauptgrp_list, t_l_lager_list

        return {"from_grp": from_grp, "to_date": to_date, "from_date": from_date, "long_digit": long_digit, "t-l-hauptgrp": t_l_hauptgrp_list, "t-l-lager": t_l_lager_list}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
    from_grp = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    to_date = htparam.fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        buffer_copy(l_hauptgrp, t_l_hauptgrp)

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    return generate_output()