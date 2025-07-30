#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, L_lager, Bediener, Htparam, Parameters, L_artikel, L_bestand

def prepare_ins_storerequestbl(user_init:string, t_datum:date, t_lschein:string):

    prepare_cache ([L_lager, Bediener, Htparam, Parameters, L_artikel, L_bestand])

    deptname = ""
    curr_lager = 0
    deptno = 0
    show_price = False
    req_flag = False
    p_220 = 0
    out_type = 1
    transfered = False
    to_stock = 0
    lager_bezeich = ""
    lager_bez1 = ""
    curr_pos = 0
    t_amount = to_decimal("0.0")
    lscheinnr = ""
    op_list_data = []
    l_op = l_lager = bediener = htparam = parameters = l_artikel = l_bestand = None

    op_list = t_l_lager = sys_user = None

    op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "new_flag":bool}, {"new_flag": True})
    t_l_lager_data, T_l_lager = create_model_like(L_lager)

    Sys_user = create_buffer("Sys_user",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal deptname, curr_lager, deptno, show_price, req_flag, p_220, out_type, transfered, to_stock, lager_bezeich, lager_bez1, curr_pos, t_amount, lscheinnr, op_list_data, l_op, l_lager, bediener, htparam, parameters, l_artikel, l_bestand
        nonlocal user_init, t_datum, t_lschein
        nonlocal sys_user


        nonlocal op_list, t_l_lager, sys_user
        nonlocal op_list_data, t_l_lager_data

        # return {"deptname": deptname, "curr_lager": curr_lager, "deptno": deptno, "show_price": show_price, "req_flag": req_flag, "p_220": p_220, "out_type": out_type, "transfered": transfered, "to_stock": to_stock, "lager_bezeich": lager_bezeich, "lager_bez1": lager_bez1, "curr_pos": curr_pos, "t_amount": t_amount, "lscheinnr": lscheinnr, "op-list": op_list_data}

        return {"deptname": deptname, "currLager": curr_lager, "deptNo": deptno, "showPrice": show_price, "reqFlag": req_flag, "p220": p_220, "outType": out_type, "transfered": transfered, "toStock": to_stock, "lagerBezeich": lager_bezeich, "lagerBez1": lager_bez1, "currPos": curr_pos, "tAmount": t_amount, "lscheinnr": lscheinnr, "opList": op_list_data}

    def read_data():

        nonlocal deptname, curr_lager, deptno, show_price, req_flag, p_220, out_type, transfered, to_stock, lager_bezeich, lager_bez1, curr_pos, t_amount, lscheinnr, op_list_data, l_op, l_lager, bediener, htparam, parameters, l_artikel, l_bestand
        nonlocal user_init, t_datum, t_lschein
        nonlocal sys_user


        nonlocal op_list, t_l_lager, sys_user
        nonlocal op_list_data, t_l_lager_data


        lscheinnr = t_lschein

        l_op = get_cache (L_op, {"datum": [(eq, t_datum)],"lscheinnr": [(eq, t_lschein)],"pos": [(gt, 0)]})

        if l_op:
            curr_lager = l_op.lager_nr
            deptno = l_op.reorgflag

            parameters = db_session.query(Parameters).filter(
                     (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (to_int(Parameters.varname) == deptno)).first()

            if parameters:
                deptname = parameters.vstring

            if l_op.op_art == 14:
                transfered = True
                out_type = 1
                to_stock = l_op.pos


            else:
                out_type = 2

            l_lager = get_cache (L_lager, {"lager_nr": [(eq, curr_lager)]})

            if l_lager:
                lager_bezeich = l_lager.bezeich

                if to_stock != 0:

                    l_lager = get_cache (L_lager, {"lager_nr": [(eq, to_stock)]})
                    lager_bez1 = l_lager.bezeich

            for l_op in db_session.query(L_op).filter(
                     (L_op.datum == t_datum) & (L_op.lscheinnr == (t_lschein).lower()) & (L_op.pos > 0) & (L_op.loeschflag <= 1)).order_by(L_op.pos).all():
                op_list = Op_list()
                op_list_data.append(op_list)

                buffer_copy(l_op, op_list)

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, l_op.artnr)]})

                sys_user = get_cache (Bediener, {"nr": [(eq, l_op.fuellflag)]})

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_op.artnr)],"lager_nr": [(eq, curr_lager)]})
                op_list.bezeich = l_artikel.bezeich
                op_list.username = sys_user.username
                op_list.new_flag = False
                curr_pos = l_op.pos
                t_amount =  to_decimal(t_amount) + to_decimal(l_op.warenwert)


                if l_bestand:
                    op_list.onhand =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:

        if substring(bediener.permissions, 21, 1) != ("0").lower() :
            show_price = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})

    if htparam:
        show_price = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 475)]})

    if htparam:
        req_flag = not htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 220)]})

    if htparam:
        p_220 = htparam.finteger
    read_data()

    return generate_output()