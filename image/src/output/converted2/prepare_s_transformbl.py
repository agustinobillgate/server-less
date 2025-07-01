#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, L_ophdr, Htparam, Gl_acct, L_lager

def prepare_s_transformbl():

    prepare_cache ([Htparam, Gl_acct, L_lager])

    wip_acct = ""
    req_flag = False
    billdate = None
    closedate = None
    mat_closedate = None
    transdate = None
    err_code = 0
    t_l_lager_list = []
    t_l_ophdr_list = []
    t_bediener_list = []
    bediener = l_ophdr = htparam = gl_acct = l_lager = None

    t_bediener = t_l_ophdr = t_l_lager = None

    t_bediener_list, T_bediener = create_model_like(Bediener)
    t_l_ophdr_list, T_l_ophdr = create_model_like(L_ophdr, {"rec_id":int})
    t_l_lager_list, T_l_lager = create_model("T_l_lager", {"lager_nr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal wip_acct, req_flag, billdate, closedate, mat_closedate, transdate, err_code, t_l_lager_list, t_l_ophdr_list, t_bediener_list, bediener, l_ophdr, htparam, gl_acct, l_lager


        nonlocal t_bediener, t_l_ophdr, t_l_lager
        nonlocal t_bediener_list, t_l_ophdr_list, t_l_lager_list

        return {"wip_acct": wip_acct, "req_flag": req_flag, "billdate": billdate, "closedate": closedate, "mat_closedate": mat_closedate, "transdate": transdate, "err_code": err_code, "t-l-lager": t_l_lager_list, "t-l-ophdr": t_l_ophdr_list, "t-bediener": t_bediener_list}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 2000)]})

    if htparam.flogical:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1201)]})

        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, htparam.fchar)]})

        if not gl_acct:
            err_code = 1

            return generate_output()

        elif gl_acct.acc_type != 3:
            err_code = 2

            return generate_output()
        wip_acct = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 475)]})
    req_flag = not htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})
    closedate = htparam.fdate

    if billdate > closedate:
        billdate = closedate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    mat_closedate = htparam.fdate
    transdate = billdate

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        t_l_lager.lager_nr = l_lager.lager_nr
        t_l_lager.bezeich = l_lager.bezeich


    l_ophdr = L_ophdr()
    db_session.add(l_ophdr)

    pass
    t_l_ophdr = T_l_ophdr()
    t_l_ophdr_list.append(t_l_ophdr)

    buffer_copy(l_ophdr, t_l_ophdr)
    t_l_ophdr.rec_id = l_ophdr._recid

    for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
        t_bediener = T_bediener()
        t_bediener_list.append(t_bediener)

        buffer_copy(bediener, t_bediener)

    return generate_output()