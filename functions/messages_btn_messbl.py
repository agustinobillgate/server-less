#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.intevent_1 import intevent_1
from models import Messages, Res_line, Htparam

def messages_btn_messbl(t_messages_resnr:int, t_messages_reslinnr:int, rec_id:int):

    prepare_cache ([Messages, Res_line, Htparam])

    messages = res_line = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal messages, res_line, htparam
        nonlocal t_messages_resnr, t_messages_reslinnr, rec_id

        return {}


    messages = get_cache (Messages, {"_recid": [(eq, rec_id)]})

    if messages:
        pass
        messages.betriebsnr = 1
        pass

    res_line = get_cache (Res_line, {"resnr": [(eq, t_messages_resnr)],"reslinnr": [(eq, t_messages_reslinnr)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 310)]})

    if htparam.flogical and res_line.active_flag == 1:
        get_output(intevent_1(5, res_line.zinr, "Message Lamp off!", res_line.resnr, res_line.reslinnr))
    pass
    res_line.wabkurz = ""
    pass

    return generate_output()