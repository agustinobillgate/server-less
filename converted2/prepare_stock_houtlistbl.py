#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_hauptgrp, Htparam, L_untergrup, Parameters

def prepare_stock_houtlistbl(lnl_filepath:string, lnl_prog:string):

    prepare_cache ([Htparam, Parameters])

    long_digit = False
    avail_l_untergrup = False
    t_l_hauptgrp_data = []
    t_parameters_data = []
    l_hauptgrp = htparam = l_untergrup = parameters = None

    t_parameters = t_l_hauptgrp = None

    t_parameters_data, T_parameters = create_model("T_parameters", {"varname":string, "vstring":string})
    t_l_hauptgrp_data, T_l_hauptgrp = create_model_like(L_hauptgrp)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal long_digit, avail_l_untergrup, t_l_hauptgrp_data, t_parameters_data, l_hauptgrp, htparam, l_untergrup, parameters
        nonlocal lnl_filepath, lnl_prog


        nonlocal t_parameters, t_l_hauptgrp
        nonlocal t_parameters_data, t_l_hauptgrp_data

        return {"lnl_filepath": lnl_filepath, "long_digit": long_digit, "avail_l_untergrup": avail_l_untergrup, "t-l-hauptgrp": t_l_hauptgrp_data, "t-parameters": t_parameters_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    l_untergrup = get_cache (L_untergrup, {"betriebsnr": [(eq, 1)]})

    if l_untergrup:
        avail_l_untergrup = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 417)]})

    if htparam.fchar != "":
        lnl_filepath = htparam.fchar

        if substring(lnl_filepath, length(lnl_filepath) - 1, 1) != ("\\").lower() :
            lnl_filepath = lnl_filepath + "\\"
        lnl_filepath = lnl_filepath + lnl_prog

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower())).order_by(Parameters._recid).all():
        t_parameters = T_parameters()
        t_parameters_data.append(t_parameters)

        t_parameters.varname = parameters.varname
        t_parameters.vstring = parameters.vstring

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        t_l_hauptgrp = T_l_hauptgrp()
        t_l_hauptgrp_data.append(t_l_hauptgrp)

        buffer_copy(l_hauptgrp, t_l_hauptgrp)

    return generate_output()