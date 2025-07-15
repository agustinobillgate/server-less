#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_op, L_artikel, Bediener

op_list_data, Op_list = create_model_like(L_op, {"bezeich":string, "username":string})

def dml_issue_create_op_listbl(op_list_data:[Op_list]):

    prepare_cache ([L_artikel, Bediener])

    l_op = l_artikel = bediener = None

    op_list = l_artikel = sys_user = buf_op_list = None

    buf_op_list_data, Buf_op_list = create_model_like(Op_list)

    L_art = create_buffer("L_art",L_artikel)
    Sys_user = create_buffer("Sys_user",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_op, l_artikel, bediener
        nonlocal l_artikel, sys_user


        nonlocal op_list, l_artikel, sys_user, buf_op_list
        nonlocal buf_op_list_data

        return {"op-list": op_list_data}


    for op_list in query(op_list_data):
        buf_op_list = Buf_op_list()
        buf_op_list_data.append(buf_op_list)

        buffer_copy(op_list, buf_op_list)
    op_list_data.clear()

    l_art_obj_list = {}
    for l_artikel, sys_user in db_session.query(L_art, Sys_user).join(Sys_user,(Sys_user.nr == buf_op_list.fuellflag)).filter(
             ((L_art.artnr.in_(list(set([buf_op_list.artnr for buf_op_list in buf_op_list_data])))))).order_by(buf_op_list.datum.desc(), buf_op_list.zeit.desc()).all():
        if l_art_obj_list.get(l_artikel._recid):
            continue
        else:
            l_art_obj_list[l_artikel._recid] = True


        op_list = Op_list()
        op_list_data.append(op_list)

        buffer_copy(buf_op_list, op_list)
        op_list.bezeich = l_artikel.bezeich
        op_list.username = sys_user.username

    return generate_output()