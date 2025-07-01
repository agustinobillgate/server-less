#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.htplogic import htplogic
from models import L_lager, L_hauptgrp

def prepare_min_onhandbl():

    prepare_cache ([L_lager, L_hauptgrp])

    show_price = False
    t_l_lager_list = []
    t_l_hauptgrp_list = []
    l_lager = l_hauptgrp = None

    t_l_lager = t_l_hauptgrp = None

    t_l_lager_list, T_l_lager = create_model("T_l_lager", {"lager_nr":int, "bezeich":string})
    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, t_l_lager_list, t_l_hauptgrp_list, l_lager, l_hauptgrp


        nonlocal t_l_lager, t_l_hauptgrp
        nonlocal t_l_lager_list, t_l_hauptgrp_list

        return {"show_price": show_price, "t-l-lager": t_l_lager_list, "t-l-hauptgrp": t_l_hauptgrp_list}

    show_price = get_output(htplogic(43))

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

    return generate_output()