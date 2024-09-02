from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_hauptgrp, Htparam, L_untergrup, Parameters

def prepare_stock_houtlistbl(lnl_filepath:str, lnl_prog:str):
    long_digit = False
    avail_l_untergrup = False
    t_l_hauptgrp_list = []
    t_parameters_list = []
    l_hauptgrp = htparam = l_untergrup = parameters = None

    t_parameters = t_l_hauptgrp = None

    t_parameters_list, T_parameters = create_model("T_parameters", {"varname":str, "vstring":str})
    t_l_hauptgrp_list, T_l_hauptgrp = create_model_like(L_hauptgrp)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, avail_l_untergrup, t_l_hauptgrp_list, t_parameters_list, l_hauptgrp, htparam, l_untergrup, parameters


        nonlocal t_parameters, t_l_hauptgrp
        nonlocal t_parameters_list, t_l_hauptgrp_list
        return {"long_digit": long_digit, "avail_l_untergrup": avail_l_untergrup, "t-l-hauptgrp": t_l_hauptgrp_list, "t-parameters": t_parameters_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    l_untergrup = db_session.query(L_untergrup).filter(
            (L_untergrup.betriebsnr == 1)).first()

    if l_untergrup:
        avail_l_untergrup = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 417)).first()

    if htparam.fchar != "":
        lnl_filepath = htparam.fchar

        if substring(lnl_filepath, len(lnl_filepath) - 1, 1) != "\\":
            lnl_filepath = lnl_filepath + "\\"
        lnl_filepath = lnl_filepath + lnl_prog

    for parameters in db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name")).all():
        t_parameters = T_parameters()
        t_parameters_list.append(t_parameters)

        t_parameters.varname = parameters.varname
        t_parameters.vstring = parameters.vstring

    for l_hauptgrp in db_session.query(L_hauptgrp).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_list.append(t_l_hauptgrp)

        buffer_copy(l_hauptgrp, t_l_hauptgrp)

    return generate_output()