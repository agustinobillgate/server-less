#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Gl_acct, L_lieferant

def prepare_mk_apbl():

    prepare_cache ([Htparam, Gl_acct])

    closed_date = None
    rgdatum = None
    p_2000 = False
    av_gl_acct = False
    ap_acct = ""
    ap_other = ""
    gst_flag = False
    htparam = gl_acct = l_lieferant = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal closed_date, rgdatum, p_2000, av_gl_acct, ap_acct, ap_other, gst_flag, htparam, gl_acct, l_lieferant

        return {"closed_date": closed_date, "rgdatum": rgdatum, "p_2000": p_2000, "av_gl_acct": av_gl_acct, "ap_acct": ap_acct, "ap_other": ap_other, "gst_flag": gst_flag}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    closed_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    rgdatum = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 2000)]})
    p_2000 = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 986)]})

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

    if not gl_acct:
        av_gl_acct = False
    else:
        av_gl_acct = True
        ap_acct = gl_acct.fibukonto

    htparam = get_cache (Htparam, {"paramnr": [(eq, 395)]})

    gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

    if gl_acct:
        ap_other = gl_acct.fibukonto
    else:
        ap_other = ap_acct

    l_lieferant = get_cache (L_lieferant, {"firma": [(eq, "gst")]})

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()