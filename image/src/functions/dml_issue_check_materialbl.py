from functions.additional_functions import *
import decimal
from models import L_op, L_artikel

def dml_issue_check_materialbl(op_list:[Op_list], mat_grp:int):
    its_ok = False
    l_op = l_artikel = None

    op_list = None

    op_list_list, Op_list = create_model_like(L_op)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, l_op, l_artikel


        nonlocal op_list
        nonlocal op_list_list
        return {"its_ok": its_ok}

    for op_list in query(op_list_list):
        l_artikel = db_session.query(L_artikel).filter((L_artikel.artnr == op_list.artnr) &  (L_artikel.endkum >= mat_grp)).first()
        if not l_artikel:
            continue

        its_ok = False

        return generate_output()