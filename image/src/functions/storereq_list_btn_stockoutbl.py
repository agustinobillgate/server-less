from functions.additional_functions import *
import decimal
from models import L_op

def storereq_list_btn_stockoutbl(t_list_s_recid:int):
    herkunftflag = 0
    l_op = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal herkunftflag, l_op


        return {"herkunftflag": herkunftflag}


    l_op = db_session.query(L_op).filter(
            (L_op._recid == t_list_s_recid)).first()
    herkunftflag = l_op.herkunftflag

    return generate_output()