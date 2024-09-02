from functions.additional_functions import *
import decimal
from datetime import date
from models import L_lager, Htparam, L_untergrup, L_hauptgrp

def prepare_sall_onhandbl():
    show_price = False
    avail_l_untergrup = False
    p_224 = None
    t_l_lager_list = []
    t_l_hauptgrp_list = []
    l_lager = htparam = l_untergrup = l_hauptgrp = None

    t_l_lager = t_l_hauptgrp = None

    t_l_lager_list, T_l_lager = create_model_like(L_lager)
    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, avail_l_untergrup, p_224, t_l_lager_list, t_l_hauptgrp_list, l_lager, htparam, l_untergrup, l_hauptgrp


        nonlocal t_l_lager, t_l_hauptgrp
        nonlocal t_l_lager_list, t_l_hauptgrp_list
        return {"show_price": show_price, "avail_l_untergrup": avail_l_untergrup, "p_224": p_224, "t-l-lager": t_l_lager_list, "t-l-hauptgrp": t_l_hauptgrp_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()
    p_224 = fdate

    l_untergrup = db_session.query(L_untergrup).filter(
            (L_untergrup.betriebsnr == 1)).first()

    if l_untergrup:
        avail_l_untergrup = True

    for l_lager in db_session.query(L_lager).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for l_hauptgrp in db_session.query(L_hauptgrp).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        buffer_copy(l_hauptgrp, t_l_hauptgrp)

    return generate_output()