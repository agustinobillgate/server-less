from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_lager, L_hauptgrp, L_lieferant

def prepare_supply_hinlist_1bl():
    t_l_lager_list = []
    t_l_hauptgrp_list = []
    gst_flag = False
    l_lager = l_hauptgrp = l_lieferant = None

    t_l_lager = t_l_hauptgrp = None

    t_l_lager_list, T_l_lager = create_model_like(L_lager)
    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_lager_list, t_l_hauptgrp_list, gst_flag, l_lager, l_hauptgrp, l_lieferant


        nonlocal t_l_lager, t_l_hauptgrp
        nonlocal t_l_lager_list, t_l_hauptgrp_list
        return {"t-l-lager": t_l_lager_list, "t-l-hauptgrp": t_l_hauptgrp_list, "gst_flag": gst_flag}


    for l_lager in db_session.query(L_lager).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for l_hauptgrp in db_session.query(L_hauptgrp).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        buffer_copy(l_hauptgrp, t_l_hauptgrp)

    l_lieferant = db_session.query(L_lieferant).filter(
            (func.lower(L_lieferant.firma) == "GST")).first()

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()