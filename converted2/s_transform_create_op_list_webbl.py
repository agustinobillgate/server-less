#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op, Bediener, L_artikel

op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "userinit":string})

def s_transform_create_op_list_webbl(op_list_data:[Op_list], qty:Decimal, price:Decimal, curr_lager:int, transdate:date, s_artnr:int, bediener_nr:string, lscheinnr:string, t_amount:Decimal):

    prepare_cache ([Bediener, L_artikel])

    amount = to_decimal("0.0")
    err_code = 0
    t_op_list_data = []
    l_op = bediener = l_artikel = None

    out_list = op_list = t_op_list = sys_user = None

    out_list_data, Out_list = create_model("Out_list", {"artnr":int})
    t_op_list_data, T_op_list = create_model_like(Op_list)

    Sys_user = create_buffer("Sys_user",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, err_code, t_op_list_data, l_op, bediener, l_artikel
        nonlocal qty, price, curr_lager, transdate, s_artnr, bediener_nr, lscheinnr, t_amount
        nonlocal sys_user


        nonlocal out_list, op_list, t_op_list, sys_user
        nonlocal out_list_data, t_op_list_data

        return {"t_amount": t_amount, "amount": amount, "err_code": err_code, "t-op-list": t_op_list_data}

    def create_op_list():

        nonlocal amount, err_code, t_op_list_data, l_op, bediener, l_artikel
        nonlocal qty, price, curr_lager, transdate, s_artnr, bediener_nr, lscheinnr, t_amount
        nonlocal sys_user


        nonlocal out_list, op_list, t_op_list, sys_user
        nonlocal out_list_data, t_op_list_data

        anzahl:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        oh_ok:bool = True
        anzahl =  to_decimal(qty)
        wert =  to_decimal(qty) * to_decimal(price)
        amount =  to_decimal(wert)
        t_amount =  to_decimal(t_amount) + to_decimal(wert)

        if curr_lager == 0:
            err_code = 1

            return
        op_list = Op_list()
        op_list_data.append(op_list)

        op_list.datum = transdate
        op_list.lager_nr = curr_lager
        op_list.artnr = s_artnr
        op_list.zeit = get_current_time_in_seconds()
        op_list.anzahl =  to_decimal(anzahl)
        op_list.einzelpreis =  to_decimal(price)
        op_list.warenwert =  to_decimal(wert)
        op_list.op_art = 4
        op_list.herkunftflag = 3
        op_list.lscheinnr = lscheinnr
        op_list.userinit = bediener_nr
        op_list.pos = 1

    create_op_list()

    l_artikel_obj_list = {}
    for l_artikel, sys_user in db_session.query(L_artikel, Sys_user).join(Sys_user,(Sys_user.userinit == op_list.userinit ORDER)).filter(
             ((L_artikel.artnr.in_(list(set([op_list.artnr for op_list in op_list_data])))))).order_by(op_list.pos.desc()).all():
        if l_artikel_obj_list.get(l_artikel._recid):
            continue
        else:
            l_artikel_obj_list[l_artikel._recid] = True


        t_op_list = T_op_list()
        t_op_list_data.append(t_op_list)

        buffer_copy(op_list, t_op_list)
        t_op_list.bezeich = l_artikel.bezeich
        t_op_list.username = sys_user.username

    return generate_output()