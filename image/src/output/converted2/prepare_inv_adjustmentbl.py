#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_hauptgrp, L_lager

def prepare_inv_adjustmentbl():

    prepare_cache ([Htparam, L_hauptgrp, L_lager])

    billdate = None
    mat_grp = 0
    early_adjust = False
    inv_postdate = None
    transdate = None
    t_l_hauptgrp_list = []
    t_l_lager_list = []
    htparam = l_hauptgrp = l_lager = None

    t_l_lager = t_l_hauptgrp = None

    t_l_lager_list, T_l_lager = create_model("T_l_lager", {"lager_nr":int, "bezeich":string})
    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, mat_grp, early_adjust, inv_postdate, transdate, t_l_hauptgrp_list, t_l_lager_list, htparam, l_hauptgrp, l_lager


        nonlocal t_l_lager, t_l_hauptgrp
        nonlocal t_l_lager_list, t_l_hauptgrp_list

        return {"billdate": billdate, "mat_grp": mat_grp, "early_adjust": early_adjust, "inv_postdate": inv_postdate, "transdate": transdate, "t-l-hauptgrp": t_l_hauptgrp_list, "t-l-lager": t_l_lager_list}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 268)]})
    mat_grp = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 401)]})

    if htparam.paramgruppe == 21:
        early_adjust = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    inv_postdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    transdate = htparam.fdate

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        t_l_hauptgrp.endkum = l_hauptgrp.endkum
        t_l_hauptgrp.bezeich = l_hauptgrp.bezeich

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        t_l_lager.lager_nr = l_lager.lager_nr
        t_l_lager.bezeich = l_lager.bezeich

    return generate_output()