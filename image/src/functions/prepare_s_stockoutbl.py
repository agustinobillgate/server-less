from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, Htparam, L_op, L_lager

def prepare_s_stockoutbl(user_init:str, t_lschein:str, out_type:int, t_datum:date):
    show_price = False
    req_flag = False
    billdate = None
    closedate = None
    mat_closedate = None
    p_221 = None
    temp_bediener_list = []
    t_l_lager_list = []
    op_num:int = 14
    bediener = htparam = l_op = l_lager = None

    t_l_lager = temp_bediener = None

    t_l_lager_list, T_l_lager = create_model("T_l_lager", {"lager_nr":int, "bezeich":str})
    temp_bediener_list, Temp_bediener = create_model_like(Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, req_flag, billdate, closedate, mat_closedate, p_221, temp_bediener_list, t_l_lager_list, op_num, bediener, htparam, l_op, l_lager


        nonlocal t_l_lager, temp_bediener
        nonlocal t_l_lager_list, temp_bediener_list
        return {"show_price": show_price, "req_flag": req_flag, "billdate": billdate, "closedate": closedate, "mat_closedate": mat_closedate, "p_221": p_221, "temp-bediener": temp_bediener_list, "t-l-lager": t_l_lager_list}


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 475)).first()
    req_flag = not htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 221)).first()
    p_221 = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 474)).first()
    billdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 221)).first()
    mat_closedate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 224)).first()

    if t_lschein != "":

        if out_type == 2:
            op_num = 13

        l_op = db_session.query(L_op).filter(
                (L_op.artnr >= 3000000) &  (L_op.datum == t_datum) &  (L_op.op_art == op_num) &  (func.lower(L_op.lscheinnr) == (t_lschein).lower())).first()

        if l_op:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 221)).first()
    closedate = htparam.fdate

    if billdate > closedate:
        billdate = closedate

    for bediener in db_session.query(Bediener).all():
        temp_bediener = Temp_bediener()
        temp_bediener_list.append(temp_bediener)

        buffer_copy(bediener, temp_bediener)

    for l_lager in db_session.query(L_lager).all():
        t_l_lager = T_l_lager()
        t_l_lager_list.append(t_l_lager)

        t_l_lager.lager_nr = l_lager.lager_nr
        t_l_lager.bezeich = l_lager.bezeich

    return generate_output()