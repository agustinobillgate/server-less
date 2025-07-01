#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htplogic import htplogic
from models import L_lager, L_untergrup, L_hauptgrp

def prepare_sall_onhandhisbl():
    show_price = False
    avail_l_untergrup = False
    t_l_lager_list = []
    t_l_hauptgrp_list = []
    l_lager = l_untergrup = l_hauptgrp = None

    t_l_lager = t_l_hauptgrp = None

    t_l_lager_list, T_l_lager = create_model_like(L_lager)
    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, avail_l_untergrup, t_l_lager_list, t_l_hauptgrp_list, l_lager, l_untergrup, l_hauptgrp


        nonlocal t_l_lager, t_l_hauptgrp
        nonlocal t_l_lager_list, t_l_hauptgrp_list

        return {"show_price": show_price, "avail_l_untergrup": avail_l_untergrup, "t-l-lager": t_l_lager_list, "t-l-hauptgrp": t_l_hauptgrp_list}

    show_price = get_output(htplogic(43))

    l_untergrup = get_cache (L_untergrup, {"betriebsnr": [(eq, 1)]})

    if l_untergrup:
        avail_l_untergrup = True

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        buffer_copy(l_hauptgrp, t_l_hauptgrp)

    return generate_output()