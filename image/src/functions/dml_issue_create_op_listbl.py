from functions.additional_functions import *
import decimal
from models import L_op, L_artikel, Bediener

def dml_issue_create_op_listbl(op_list:[Op_list]):
    l_op = l_artikel = bediener = None

    op_list = l_artikel = sys_user = buf_op_list = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str})
    buf_op_list_list, Buf_op_list = create_model_like(Op_list)

    L_art = L_artikel
    Sys_user = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_op, l_artikel, bediener
        nonlocal l_artikel, sys_user


        nonlocal op_list, l_artikel, sys_user, buf_op_list
        nonlocal op_list_list, buf_op_list_list
        return {}


    for op_list in query(op_list_list):
        buf_op_list = Buf_op_list()
        buf_op_list_list.append(buf_op_list)

        buffer_copy(op_list, buf_op_list)
    op_list_list.clear()

    for buf_op_list in query(buf_op_list_list):
        l_artikel = db_session.query(L_art).filter((L_art.artnr == buf_op_list.artnr)).first()
        if not l_artikel:
            continue

        sys_user = db_session.query(Sys_user).filter((Sys_user.nr == buf_op_list.fuellflag)).first()
        if not sys_user:
            continue

        op_list = Op_list()
        op_list_list.append(op_list)

        buffer_copy(buf_op_list, op_list)
        op_list.bezeich = l_artikel.bezeich
        op_list.username = sys_user.username

    return generate_output()