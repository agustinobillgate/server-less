from functions.additional_functions import *
import decimal
from datetime import date
from models import L_op, Bediener, L_artikel

def s_transform_create_op_listbl(op_list:[Op_list], qty:decimal, price:decimal, curr_lager:int, transdate:date, s_artnr:int, bediener_nr:int, lscheinnr:str, t_amount:decimal):
    amount = 0
    err_code = 0
    t_op_list_list = []
    l_op = bediener = l_artikel = None

    out_list = op_list = t_op_list = sys_user = None

    out_list_list, Out_list = create_model("Out_list", {"artnr":int})
    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str})
    t_op_list_list, T_op_list = create_model_like(Op_list)

    Sys_user = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, err_code, t_op_list_list, l_op, bediener, l_artikel
        nonlocal sys_user


        nonlocal out_list, op_list, t_op_list, sys_user
        nonlocal out_list_list, op_list_list, t_op_list_list
        return {"amount": amount, "err_code": err_code, "t-op-list": t_op_list_list}

    def create_op_list():

        nonlocal amount, err_code, t_op_list_list, l_op, bediener, l_artikel
        nonlocal sys_user


        nonlocal out_list, op_list, t_op_list, sys_user
        nonlocal out_list_list, op_list_list, t_op_list_list

        anzahl:decimal = 0
        wert:decimal = 0
        oh_ok:bool = True
        anzahl = qty
        wert = qty * price
        amount = wert
        t_amount = t_amount + wert

        if curr_lager == 0:
            err_code = 1

            return
        op_list = Op_list()
        op_list_list.append(op_list)

        op_list.datum = transdate
        op_list.lager_nr = curr_lager
        op_list.artnr = s_artnr
        op_list.zeit = get_current_time_in_seconds()
        op_list.anzahl = anzahl
        op_list.einzelpreis = price
        op_list.warenwert = wert
        op_list.op_art = 4
        op_list.herkunftflag = 3
        op_list.lscheinnr = lscheinnr
        op_list.fuellflag = bediener_nr
        op_list.pos = 1


    create_op_list()

    for op_list in query(op_list_list):
        l_artikel = db_session.query(L_artikel).filter((l_artikel.artnr == op_list.artnr)).first()
        if not l_artikel:
            continue

        sys_user = db_session.query(Sys_user).filter((Sys_user.nr == op_list.fuellflag)).first()
        if not sys_user:
            continue

        t_op_list = T_op_list()
        t_op_list_list.append(t_op_list)

        buffer_copy(op_list, t_op_list)
        t_op_list.bezeich = l_artikel.bezeich
        t_op_list.username = sys_user.username

    return generate_output()