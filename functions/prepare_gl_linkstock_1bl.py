#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_hauptgrp

def prepare_gl_linkstock_1bl(link_in:bool):

    prepare_cache ([Htparam, L_hauptgrp])

    f_int = 0
    jtype = 0
    last_acctdate = None
    acct_date = None
    close_year = None
    msg_str = ""
    l_hauptgrp_list_data = []
    last_acct_period:date = None
    tmpdate:date = None
    htparam = l_hauptgrp = None

    l_hauptgrp_list = None

    l_hauptgrp_list_data, L_hauptgrp_list = create_model("L_hauptgrp_list", {"endkum":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_int, jtype, last_acctdate, acct_date, close_year, msg_str, l_hauptgrp_list_data, last_acct_period, tmpdate, htparam, l_hauptgrp
        nonlocal link_in


        nonlocal l_hauptgrp_list
        nonlocal l_hauptgrp_list_data

        return {"f_int": f_int, "jtype": jtype, "last_acctdate": last_acctdate, "acct_date": acct_date, "close_year": close_year, "msg_str": msg_str, "l-hauptgrp-list": l_hauptgrp_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1012)]})

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1 and htparam.finteger > 0:
        f_int = htparam.finteger

    if link_in:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 269)]})
        jtype = 6
    else:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1035)]})
        jtype = 3
    last_acctdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    acct_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    close_year = htparam.fdate

    for l_hauptgrp in db_session.query(L_hauptgrp).order_by(L_hauptgrp._recid).all():
        l_hauptgrp_list = L_hauptgrp_list()
        l_hauptgrp_list_data.append(l_hauptgrp_list)

        l_hauptgrp_list.endkum = l_hauptgrp.endkum
        l_hauptgrp_list.bezeich = l_hauptgrp.bezeich

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    last_acct_period = htparam.fdate
    tmpdate = last_acctdate + timedelta(days=1)

    if tmpdate <= last_acct_period:
        msg_str = "Last INV transfer to GL (Param 269 / Param 1035) lower THEN last accounting closing period (Param 558)." + chr_unicode(10) + "Transfer to GL not possible."

        return generate_output()

    return generate_output()