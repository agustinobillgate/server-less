#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, L_lager, L_hauptgrp, L_untergrup

def prepare_slow_moving_1bl(lnl_prog:string):

    prepare_cache ([Htparam, L_lager, L_hauptgrp, L_untergrup])

    lnl_filepath = ""
    show_price = False
    t_l_lager_list = []
    t_l_hauptgrp_list = []
    t_l_untergrup_list = []
    htparam = l_lager = l_hauptgrp = l_untergrup = None

    t_l_lager = t_l_hauptgrp = t_l_untergrup = None

    t_l_lager_list, T_l_lager = create_model("T_l_lager", {"lager_nr":int, "bezeich":string})
    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":string})
    t_l_untergrup_list, T_l_untergrup = create_model("T_l_untergrup", {"zwkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lnl_filepath, show_price, t_l_lager_list, t_l_hauptgrp_list, t_l_untergrup_list, htparam, l_lager, l_hauptgrp, l_untergrup
        nonlocal lnl_prog


        nonlocal t_l_lager, t_l_hauptgrp, t_l_untergrup
        nonlocal t_l_lager_list, t_l_hauptgrp_list, t_l_untergrup_list

        return {"lnl_filepath": lnl_filepath, "show_price": show_price, "t-l-lager": t_l_lager_list, "t-l-hauptgrp": t_l_hauptgrp_list, "t-l-untergrup": t_l_untergrup_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 417)]})

    if htparam.fchar != "":
        lnl_filepath = htparam.fchar

        if substring(lnl_filepath, length(lnl_filepath) - 1, 1) != ("\\").lower() :
            lnl_filepath = lnl_filepath + "\\"
        lnl_filepath = lnl_filepath + lnl_prog

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

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

    for l_untergrup in db_session.query(L_untergrup).order_by(L_untergrup._recid).all():
        t_l_untergrup = T_l_untergrup()
        t_l_untergrup_list.append(t_l_untergrup)

        t_l_untergrup.zwkum = l_untergrup.zwkum
        t_l_untergrup.bezeich = l_untergrup.bezeich

    return generate_output()