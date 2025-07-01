#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_op

def storereq_list_btn_exit2bl(t_list_s_recid:int, flager:int, tlager:int):

    prepare_cache ([L_op])

    l_op = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_op
        nonlocal t_list_s_recid, flager, tlager

        return {}


    l_op = get_cache (L_op, {"_recid": [(eq, t_list_s_recid)]})
    l_op.lager_nr = flager
    l_op.pos = tlager


    pass

    return generate_output()