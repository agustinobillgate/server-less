from functions.additional_functions import *
import decimal
from models import Htparam, L_hauptgrp, L_lager

def prepare_slow_movingbl(lnl_prog:str):
    lnl_filepath = ""
    show_price = False
    t_l_lager_list = []
    t_l_hauptgrp_list = []
    htparam = l_hauptgrp = l_lager = None

    t_l_lager = t_l_hauptgrp = None

    t_l_lager_list, T_l_lager = create_model("T_l_lager", {"lager_nr":int, "bezeich":str})
    t_l_hauptgrp_list, T_l_hauptgrp = create_model("T_l_hauptgrp", {"endkum":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lnl_filepath, show_price, t_l_lager_list, t_l_hauptgrp_list, htparam, l_hauptgrp, l_lager


        nonlocal t_l_lager, t_l_hauptgrp
        nonlocal t_l_lager_list, t_l_hauptgrp_list
        return {"lnl_filepath": lnl_filepath, "show_price": show_price, "t-l-lager": t_l_lager_list, "t-l-hauptgrp": t_l_hauptgrp_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 417)).first()

    if htparam.fchar != "":
        lnl_filepath = htparam.fchar

        if substring(lnl_filepath, len(lnl_filepath) - 1, 1) != "\\":
            lnl_filepath = lnl_filepath + "\\"
        lnl_filepath = lnl_filepath + lnl_prog

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    for l_hauptgrp in db_session.query(L_hauptgrp).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        t_l_hauptgrp.endkum = l_hauptgrp.endkum
        t_l_hauptgrp.bezeich = l_hauptgrp.bezeich

    for l_lager in db_session.query(L_lager).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        t_l_lager.lager_nr = l_lager.lager_nr
        t_l_lager.bezeich = l_lager.bezeich

    return generate_output()