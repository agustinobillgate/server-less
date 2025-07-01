#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lager, L_hauptgrp, L_lieferant

def prepare_supply_hinlist_1bl():
    t_l_lager_list = []
    t_l_hauptgrp_list = []
    gst_flag = False
    l_lager = l_hauptgrp = l_lieferant = None

    t_l_lager = t_l_hauptgrp = None

    t_l_lager_list, T_l_lager = create_model_like(L_lager)
    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_lager_list, t_l_hauptgrp_list, gst_flag, l_lager, l_hauptgrp, l_lieferant


        nonlocal t_l_lager, t_l_hauptgrp
        nonlocal t_l_lager_list, t_l_hauptgrp_list

        return {"t-l-lager": t_l_lager_list, "t-l-hauptgrp": t_l_hauptgrp_list, "gst_flag": gst_flag}


    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        buffer_copy(l_hauptgrp, t_l_hauptgrp)

    l_lieferant = get_cache (L_lieferant, {"firma": [(eq, "gst")]})

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()