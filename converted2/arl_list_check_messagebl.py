#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Messages

def arl_list_check_messagebl(arl_list_resnr:int, arl_list_reslinnr:int):
    avail_msg = False
    messages = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_msg, messages
        nonlocal arl_list_resnr, arl_list_reslinnr

        return {"avail_msg": avail_msg}


    messages = get_cache (Messages, {"resnr": [(eq, arl_list_resnr)],"reslinnr": [(eq, arl_list_reslinnr)]})

    if messages:
        avail_msg = True

    return generate_output()