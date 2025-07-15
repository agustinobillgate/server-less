#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bediener

def prepare_vip_listbl(user_init:string):

    prepare_cache ([Htparam, Bediener])

    ci_date = None
    show_rate = False
    p_297 = 0
    lnl_filepath = ""
    t_vipnr_data = []
    htparam = bediener = None

    t_vipnr = None

    t_vipnr_data, T_vipnr = create_model("T_vipnr", {"vip_nr1":int, "vip_nr2":int, "vip_nr3":int, "vip_nr4":int, "vip_nr5":int, "vip_nr6":int, "vip_nr7":int, "vip_nr8":int, "vip_nr9":int, "vip_nr10":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, show_rate, p_297, lnl_filepath, t_vipnr_data, htparam, bediener
        nonlocal user_init


        nonlocal t_vipnr
        nonlocal t_vipnr_data

        return {"ci_date": ci_date, "show_rate": show_rate, "p_297": p_297, "lnl_filepath": lnl_filepath, "t-vipnr": t_vipnr_data}

    def fill_vipnr():

        nonlocal ci_date, show_rate, p_297, lnl_filepath, t_vipnr_data, htparam, bediener
        nonlocal user_init


        nonlocal t_vipnr
        nonlocal t_vipnr_data


        t_vipnr = T_vipnr()
        t_vipnr_data.append(t_vipnr)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

        if htparam:
            t_vipnr.vip_nr1 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

        if htparam:
            t_vipnr.vip_nr2 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

        if htparam:
            t_vipnr.vip_nr3 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

        if htparam:
            t_vipnr.vip_nr4 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

        if htparam:
            t_vipnr.vip_nr5 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

        if htparam:
            t_vipnr.vip_nr6 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

        if htparam:
            t_vipnr.vip_nr7 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

        if htparam:
            t_vipnr.vip_nr8 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

        if htparam:
            t_vipnr.vip_nr9 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 712)]})

        if htparam:
            t_vipnr.vip_nr10 = htparam.finteger


    htparam = get_cache (Htparam, {"paramnr": [(eq, 417)]})

    if htparam:

        if htparam.fchar != "":
            lnl_filepath = htparam.fchar

            if substring(lnl_filepath, length(lnl_filepath) - 1, 1) != ("\\").lower() :
                lnl_filepath = lnl_filepath + "\\"

    htparam = get_cache (Htparam, {"paramnr": [(eq, 297)]})

    if htparam:
        p_297 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        ci_date = htparam.fdate

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:

        if substring(bediener.permissions, 34, 1) != ("0").lower() :
            show_rate = True
    fill_vipnr()

    return generate_output()