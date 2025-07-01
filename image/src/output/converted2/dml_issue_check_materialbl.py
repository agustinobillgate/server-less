#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_op, L_artikel

op_list_list, Op_list = create_model_like(L_op)

def dml_issue_check_materialbl(op_list_list:[Op_list], mat_grp:int):
    its_ok = True
    param89:bool = False
    l_op = l_artikel = None

    op_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, param89, l_op, l_artikel
        nonlocal mat_grp


        nonlocal op_list

        return {"its_ok": its_ok}


    its_ok = False

    l_artikel_obj_list = {}
    for l_artikel in db_session.query(L_artikel).filter(
             ((L_artikel.artnr.in_(list(set([op_list.artnr for op_list in op_list_list])))))).order_by(L_artikel._recid).all():
        if l_artikel_obj_list.get(l_artikel._recid):
            continue
        else:
            l_artikel_obj_list[l_artikel._recid] = True


        its_ok = True

        return generate_output()

    return generate_output()