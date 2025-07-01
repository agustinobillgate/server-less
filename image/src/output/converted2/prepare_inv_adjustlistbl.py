#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_lager, L_hauptgrp

def prepare_inv_adjustlistbl():

    prepare_cache ([Htparam, L_lager, L_hauptgrp])

    billdate = None
    mat_grp = 0
    transdate = None
    p_221 = None
    p_224 = None
    t_l_lager_list = []
    t_l_hauptgrp_list = []
    htparam = l_lager = l_hauptgrp = None

    t_l_lager = t_l_hauptgrp = None

    t_l_lager_list, T_l_lager = create_model("T_l_lager", {"lager_nr":int, "bezeich":string})
    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, mat_grp, transdate, p_221, p_224, t_l_lager_list, t_l_hauptgrp_list, htparam, l_lager, l_hauptgrp


        nonlocal t_l_lager, t_l_hauptgrp
        nonlocal t_l_lager_list, t_l_hauptgrp_list

        return {"billdate": billdate, "mat_grp": mat_grp, "transdate": transdate, "p_221": p_221, "p_224": p_224, "t-l-lager": t_l_lager_list, "t-l-hauptgrp": t_l_hauptgrp_list}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})

    if htparam:
        mat_grp = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})

    if htparam:
        transdate = htparam.fdate

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        t_l_lager.lager_nr = l_lager.lager_nr
        t_l_lager.bezeich = l_lager.bezeich

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        t_l_hauptgrp.endkum = l_hauptgrp.endkum
        t_l_hauptgrp.bezeich = l_hauptgrp.bezeich

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})

    if htparam:
        p_221 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})

    if htparam:
        p_224 = htparam.fdate

    return generate_output()