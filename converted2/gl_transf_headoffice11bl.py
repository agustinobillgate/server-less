#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.gl_transf_headoffice22bl import gl_transf_headoffice22bl
from models import Gl_acct, Gl_accthis, Htparam

def gl_transf_headoffice11bl(pvilanguage:int, close_month:date, close_year:date):

    prepare_cache ([Htparam])

    success_flag = False
    msg_str = ""
    first_date:date = None
    lreturn:bool = False
    map_acct:string = ""
    hoappparam:string = ""
    vhost:string = ""
    vservice:string = ""
    htl_code:string = ""
    lvcarea:string = "closemonth"
    gl_acct = gl_accthis = htparam = None

    t_gl_acct = t_gl_accthis = None

    t_gl_acct_data, T_gl_acct = create_model_like(Gl_acct)
    t_gl_accthis_data, T_gl_accthis = create_model_like(Gl_accthis)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, msg_str, first_date, lreturn, map_acct, hoappparam, vhost, vservice, htl_code, lvcarea, gl_acct, gl_accthis, htparam
        nonlocal pvilanguage, close_month, close_year


        nonlocal t_gl_acct, t_gl_accthis
        nonlocal t_gl_acct_data, t_gl_accthis_data

        return {"success_flag": success_flag, "msg_str": msg_str}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 2843)]})
    vhost = entry(0, htparam.fchar, ":")
    vservice = entry(1, htparam.fchar, ":")
    htl_code = entry(2, htparam.fchar, ":")
    hoappparam = " -H " + vhost + " -S " + vservice + " -DirectConnect -sessionModel Session-free"


    lreturn = set_combo_session(hoappparam, None , None , None)

    if not lreturn:
        msg_str = translateExtended ("Failed to connect to HO server", lvcarea, "") + chr_unicode(10) + translateExtended ("Journals could not be transferred to the Heaad Office DB.", lvcarea, "")


        return generate_output()

    if close_month != None:

        for gl_acct in db_session.query(Gl_acct).order_by(Gl_acct._recid).all():
            t_gl_acct = T_gl_acct()
            t_gl_acct_data.append(t_gl_acct)

            buffer_copy(gl_acct, t_gl_acct)


    if close_year != None:

        for gl_accthis in db_session.query(Gl_accthis).filter(
                 (Gl_accthis.year == get_year(close_year))).order_by(Gl_accthis._recid).all():
            t_gl_accthis = T_gl_accthis()
            t_gl_accthis_data.append(t_gl_accthis)

            buffer_copy(gl_accthis, t_gl_accthis)

    local_storage.combo_flag = True
    success_flag = get_output(gl_transf_headoffice22bl(htl_code, close_month, close_year, t_gl_acct_data, t_gl_accthis_data))
    local_storage.combo_flag = False


    if not success_flag:
        msg_str = \
            translateExtended ("Property Code not defined in the HO DB.", lvcarea, "")


    else:
        msg_str = \
            translateExtended ("GL COA have been transferred to the HO DB.", lvcarea, "")


    lreturn = reset_combo_session()


    return generate_output()