#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lager, Htparam, L_untergrup, L_hauptgrp

def prepare_sall_onhandbl():

    prepare_cache ([Htparam])

    show_price = False
    avail_l_untergrup = False
    p_224 = None
    t_l_lager_data = []
    t_l_hauptgrp_data = []
    l_lager = htparam = l_untergrup = l_hauptgrp = None

    t_l_lager = t_l_hauptgrp = None

    t_l_lager_data, T_l_lager = create_model_like(L_lager)
    t_l_hauptgrp_data, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, avail_l_untergrup, p_224, t_l_lager_data, t_l_hauptgrp_data, l_lager, htparam, l_untergrup, l_hauptgrp


        nonlocal t_l_lager, t_l_hauptgrp
        nonlocal t_l_lager_data, t_l_hauptgrp_data

        return {"show_price": show_price, "avail_l_untergrup": avail_l_untergrup, "p_224": p_224, "t-l-lager": t_l_lager_data, "t-l-hauptgrp": t_l_hauptgrp_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    p_224 = htparam.fdate

    l_untergrup = get_cache (L_untergrup, {"betriebsnr": [(eq, 1)]})

    if l_untergrup:
        avail_l_untergrup = True

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_data.append(t_l_lager)

        buffer_copy(l_lager, t_l_lager)

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_data.append(t_l_hauptgrp)

        buffer_copy(l_hauptgrp, t_l_hauptgrp)

    return generate_output()