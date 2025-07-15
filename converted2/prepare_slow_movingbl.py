#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, L_hauptgrp, L_lager

def prepare_slow_movingbl(lnl_prog:string):

    prepare_cache ([Htparam, L_hauptgrp, L_lager])

    lnl_filepath = ""
    show_price = False
    t_l_lager_data = []
    t_l_hauptgrp_data = []
    htparam = l_hauptgrp = l_lager = None

    t_l_lager = t_l_hauptgrp = None

    t_l_lager_data, T_l_lager = create_model("T_l_lager", {"lager_nr":int, "bezeich":string})
    t_l_hauptgrp_data, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lnl_filepath, show_price, t_l_lager_data, t_l_hauptgrp_data, htparam, l_hauptgrp, l_lager
        nonlocal lnl_prog


        nonlocal t_l_lager, t_l_hauptgrp
        nonlocal t_l_lager_data, t_l_hauptgrp_data

        return {"lnl_filepath": lnl_filepath, "show_price": show_price, "t-l-lager": t_l_lager_data, "t-l-hauptgrp": t_l_hauptgrp_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 417)]})

    if htparam.fchar != "":
        lnl_filepath = htparam.fchar

        if substring(lnl_filepath, length(lnl_filepath) - 1, 1) != ("\\").lower() :
            lnl_filepath = lnl_filepath + "\\"
        lnl_filepath = lnl_filepath + lnl_prog

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_data.append(t_l_hauptgrp)

        t_l_hauptgrp.endkum = l_hauptgrp.endkum
        t_l_hauptgrp.bezeich = l_hauptgrp.bezeich

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_data.append(t_l_lager)

        t_l_lager.lager_nr = l_lager.lager_nr
        t_l_lager.bezeich = l_lager.bezeich

    return generate_output()