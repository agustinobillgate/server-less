#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Htparam, L_op, L_lager

def prepare_s_stockoutbl(user_init:string, t_lschein:string, out_type:int, t_datum:date):

    prepare_cache ([Htparam, L_lager])

    show_price = False
    req_flag = False
    billdate = None
    closedate = None
    mat_closedate = None
    p_221 = None
    temp_bediener_data = []
    t_l_lager_data = []
    op_num:int = 14
    bediener = htparam = l_op = l_lager = None

    t_l_lager = temp_bediener = None

    t_l_lager_data, T_l_lager = create_model("T_l_lager", {"lager_nr":int, "bezeich":string})
    temp_bediener_data, Temp_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, req_flag, billdate, closedate, mat_closedate, p_221, temp_bediener_data, t_l_lager_data, op_num, bediener, htparam, l_op, l_lager
        nonlocal user_init, t_lschein, out_type, t_datum


        nonlocal t_l_lager, temp_bediener
        nonlocal t_l_lager_data, temp_bediener_data

        return {"show_price": show_price, "req_flag": req_flag, "billdate": billdate, "closedate": closedate, "mat_closedate": mat_closedate, "p_221": p_221, "temp-bediener": temp_bediener_data, "t-l-lager": t_l_lager_data}


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
        show_price = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 475)]})
    req_flag = not htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    p_221 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 474)]})
    billdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    mat_closedate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 224)]})

    if t_lschein != "":

        if out_type == 2:
            op_num = 13

        l_op = get_cache (L_op, {"artnr": [(ge, 3000000)],"datum": [(eq, t_datum)],"op_art": [(eq, op_num)],"lscheinnr": [(eq, t_lschein)]})

        if l_op:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 221)]})
    closedate = htparam.fdate

    if billdate > closedate:
        billdate = closedate

    for bediener in db_session.query(Bediener).order_by(Bediener._recid).all():
        temp_bediener = Temp_bediener()
        temp_bediener_data.append(temp_bediener)

        buffer_copy(bediener, temp_bediener)

    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_data.append(t_l_lager)

        t_l_lager.lager_nr = l_lager.lager_nr
        t_l_lager.bezeich = l_lager.bezeich

    return generate_output()