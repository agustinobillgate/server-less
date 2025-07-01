#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_op

def storereq_list_btn_stockoutbl(t_list_s_recid:int):

    prepare_cache ([L_op])

    herkunftflag = 0
    l_op = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal herkunftflag, l_op
        nonlocal t_list_s_recid

        return {"herkunftflag": herkunftflag}


    l_op = get_cache (L_op, {"_recid": [(eq, t_list_s_recid)]})
    herkunftflag = l_op.herkunftflag

    return generate_output()