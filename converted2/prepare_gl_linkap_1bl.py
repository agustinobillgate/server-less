#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Gl_jouhdr

def prepare_gl_linkap_1bl():

    prepare_cache ([Htparam, Gl_jouhdr])

    f_int = 0
    last_acctdate = None
    acct_date = None
    close_year = None
    msg_str = ""
    gl_jouhdr_list_data = []
    last_acct_period:date = None
    tmpdate:date = None
    htparam = gl_jouhdr = None

    gl_jouhdr_list = None

    gl_jouhdr_list_data, Gl_jouhdr_list = create_model("Gl_jouhdr_list", {"refno":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_int, last_acctdate, acct_date, close_year, msg_str, gl_jouhdr_list_data, last_acct_period, tmpdate, htparam, gl_jouhdr


        nonlocal gl_jouhdr_list
        nonlocal gl_jouhdr_list_data

        return {"f_int": f_int, "last_acctdate": last_acctdate, "acct_date": acct_date, "close_year": close_year, "msg_str": msg_str, "gl-jouhdr-list": gl_jouhdr_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1012)]})

    if htparam.paramgruppe == 38 and htparam.feldtyp == 1 and htparam.finteger > 0:
        f_int = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1118)]})
    last_acctdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    acct_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 795)]})
    close_year = htparam.fdate

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.jtype == 4)).order_by(Gl_jouhdr._recid).all():
        gl_jouhdr_list = Gl_jouhdr_list()
        gl_jouhdr_list_data.append(gl_jouhdr_list)

        gl_jouhdr_list.refno = gl_jouhdr.refno

    htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})
    last_acct_period = htparam.fdate
    tmpdate = last_acctdate + timedelta(days=1)

    if tmpdate <= last_acct_period:
        msg_str = "Last AP transfer to GL (Param 1118) lower THEN last accounting closing period (Param 558)." + chr_unicode(10) + "Transfer to GL not possible."

        return generate_output()

    return generate_output()