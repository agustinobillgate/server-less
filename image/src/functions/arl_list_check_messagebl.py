from functions.additional_functions import *
import decimal
from models import Messages

def arl_list_check_messagebl(arl_list_resnr:int, arl_list_reslinnr:int):
    avail_msg = False
    messages = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_msg, messages


        return {"avail_msg": avail_msg}


    messages = db_session.query(Messages).filter(
            (Messages.resnr == arl_list_resnr) &  (Messages.reslinnr == arl_list_reslinnr)).first()

    if messages:
        avail_msg = True

    return generate_output()