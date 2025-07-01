#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Paramtext, Htparam, Akt_line

def prepare_gcf_listbl(user_init:string):

    prepare_cache ([Paramtext, Htparam])

    sorttype_fchar0 = ""
    sorttype_fchar1 = ""
    sorttype_fchar2 = ""
    ext_char = ""
    htl_city = ""
    curr_htl_city = ""
    vhp_lite = False
    vhp_multi = False
    rest_lic = False
    long_digit = False
    aktlist_flag = False
    ci_date = None
    vipnr1 = 999999999
    vipnr2 = 999999999
    vipnr3 = 999999999
    vipnr4 = 999999999
    vipnr5 = 999999999
    vipnr6 = 999999999
    vipnr7 = 999999999
    vipnr8 = 999999999
    vipnr9 = 999999999
    paramtext = htparam = akt_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sorttype_fchar0, sorttype_fchar1, sorttype_fchar2, ext_char, htl_city, curr_htl_city, vhp_lite, vhp_multi, rest_lic, long_digit, aktlist_flag, ci_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, paramtext, htparam, akt_line
        nonlocal user_init

        return {"sorttype_fchar0": sorttype_fchar0, "sorttype_fchar1": sorttype_fchar1, "sorttype_fchar2": sorttype_fchar2, "ext_char": ext_char, "htl_city": htl_city, "curr_htl_city": curr_htl_city, "vhp_lite": vhp_lite, "vhp_multi": vhp_multi, "rest_lic": rest_lic, "long_digit": long_digit, "aktlist_flag": aktlist_flag, "ci_date": ci_date, "vipnr1": vipnr1, "vipnr2": vipnr2, "vipnr3": vipnr3, "vipnr4": vipnr4, "vipnr5": vipnr5, "vipnr6": vipnr6, "vipnr7": vipnr7, "vipnr8": vipnr8, "vipnr9": vipnr9}

    def get_vipnr():

        nonlocal sorttype_fchar0, sorttype_fchar1, sorttype_fchar2, ext_char, htl_city, curr_htl_city, vhp_lite, vhp_multi, rest_lic, long_digit, aktlist_flag, ci_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, paramtext, htparam, akt_line
        nonlocal user_init

        htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

        if htparam.finteger != 0:
            vipnr1 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

        if htparam.finteger != 0:
            vipnr2 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

        if htparam.finteger != 0:
            vipnr3 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

        if htparam.finteger != 0:
            vipnr4 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

        if htparam.finteger != 0:
            vipnr5 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

        if htparam.finteger != 0:
            vipnr6 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

        if htparam.finteger != 0:
            vipnr7 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

        if htparam.finteger != 0:
            vipnr8 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

        if htparam.finteger != 0:
            vipnr9 = htparam.finteger

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 203)]})
    curr_htl_city = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 796)]})

    if htparam.fchar != "":
        sorttype_fchar0 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 797)]})

    if htparam.fchar != "":
        sorttype_fchar1 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 798)]})

    if htparam.fchar != "":
        sorttype_fchar2 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1015)]})
    vhp_lite = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 996)]})
    vhp_multi = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 990)]})
    rest_lic = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 148)]})
    ext_char = htparam.fchar
    get_vipnr()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1355)]})

    if htparam.flogical :
        ci_date = get_current_date()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1002)]})

    if htparam.flogical:

        akt_line = get_cache (Akt_line, {"userinit": [(eq, user_init)],"datum": [(ge, ci_date - timedelta(days=1)),(le, ci_date)]})
        aktlist_flag = None != akt_line

    paramtext = get_cache (Paramtext, {"txtnr": [(ge, 203)]})
    htl_city = paramtext.ptexte

    return generate_output()