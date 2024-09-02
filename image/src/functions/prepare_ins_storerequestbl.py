from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_op, L_lager, Bediener, Htparam, Parameters, L_artikel, L_bestand

def prepare_ins_storerequestbl(user_init:str, t_datum:date, t_lschein:str):
    deptname = ""
    curr_lager = 0
    deptno = 0
    show_price = False
    req_flag = False
    p_220 = 0
    out_type = 0
    transfered = False
    to_stock = 0
    lager_bezeich = ""
    lager_bez1 = ""
    curr_pos = 0
    t_amount = 0
    lscheinnr = ""
    op_list_list = []
    l_op = l_lager = bediener = htparam = parameters = l_artikel = l_bestand = None

    op_list = t_l_lager = sys_user = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str, "onhand":decimal, "new_flag":bool}, {"new_flag": True})
    t_l_lager_list, T_l_lager = create_model_like(L_lager)

    Sys_user = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal deptname, curr_lager, deptno, show_price, req_flag, p_220, out_type, transfered, to_stock, lager_bezeich, lager_bez1, curr_pos, t_amount, lscheinnr, op_list_list, l_op, l_lager, bediener, htparam, parameters, l_artikel, l_bestand
        nonlocal sys_user


        nonlocal op_list, t_l_lager, sys_user
        nonlocal op_list_list, t_l_lager_list
        return {"deptname": deptname, "curr_lager": curr_lager, "deptno": deptno, "show_price": show_price, "req_flag": req_flag, "p_220": p_220, "out_type": out_type, "transfered": transfered, "to_stock": to_stock, "lager_bezeich": lager_bezeich, "lager_bez1": lager_bez1, "curr_pos": curr_pos, "t_amount": t_amount, "lscheinnr": lscheinnr, "op-list": op_list_list}

    def read_data():

        nonlocal deptname, curr_lager, deptno, show_price, req_flag, p_220, out_type, transfered, to_stock, lager_bezeich, lager_bez1, curr_pos, t_amount, lscheinnr, op_list_list, l_op, l_lager, bediener, htparam, parameters, l_artikel, l_bestand
        nonlocal sys_user


        nonlocal op_list, t_l_lager, sys_user
        nonlocal op_list_list, t_l_lager_list


        lscheinnr = t_lschein

        l_op = db_session.query(L_op).filter(
                (L_op.datum == t_datum) &  (func.lower(L_op.lscheinnr) == (t_lschein).lower()) &  (L_op.pos > 0)).first()
        curr_lager = l_op.lager
        deptno = l_op.reorgflag

        parameters = db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (to_int(Parameters.varname) == deptno)).first()

        if parameters:
            deptname = parameters.vstring

        if l_op.op_art == 14:
            transfered = True
            out_type = 1
            to_stock = l_op.pos


        else:
            out_type = 2

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == curr_lager)).first()
        lager_bezeich = l_lager.bezeich

        if to_stock != 0:

            l_lager = db_session.query(L_lager).filter(
                    (L_lager.lager_nr == to_stock)).first()
            lager_bez1 = l_lager.bezeich

        for l_op in db_session.query(L_op).filter(
                (L_op.datum == t_datum) &  (func.lower(L_op.lscheinnr) == (t_lschein).lower()) &  (L_op.pos > 0) &  (L_op.loeschflag <= 1)).all():
            op_list = Op_list()
            op_list_list.append(op_list)

            buffer_copy(l_op, op_list)

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == l_op.artnr)).first()

            sys_user = db_session.query(Sys_user).filter(
                    (Sys_user.nr == l_op.fuellflag)).first()

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.artnr == l_op.artnr) &  (L_bestand.lager_nr == curr_lager)).first()
            op_list.bezeich = l_artikel.bezeich
            op_list.username = sys_user.username
            op_list.new_flag = False
            curr_pos = l_op.pos
            t_amount = t_amount + l_op.warenwert


            pass

            if l_bestand:
                op_list.onhand = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang


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
            (Htparam.paramnr == 220)).first()
    p_220 = htparam.finteger
    read_data()

    return generate_output()