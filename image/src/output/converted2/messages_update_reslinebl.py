#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.intevent_1 import intevent_1
from models import Res_line, Messages

def messages_update_reslinebl(resnr:int, reslinnr:int):

    prepare_cache ([Res_line])

    res_line = messages = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line, messages
        nonlocal resnr, reslinnr

        return {}

    def update_resline():

        nonlocal res_line, messages
        nonlocal resnr, reslinnr

        messages = get_cache (Messages, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"betriebsnr": [(eq, 0)]})

        if messages:

            if res_line.wabkurz == "":
                pass
                res_line.wabkurz = "M"
                pass

                if res_line.active_flag == 1:
                    get_output(intevent_1(4, res_line.zinr, "Message Lamp on!", res_line.resnr, res_line.reslinnr))
        else:

            if res_line.wabkurz.lower()  == ("M").lower() :
                pass
                res_line.wabkurz = ""
                pass

                if res_line.active_flag == 1:
                    get_output(intevent_1(5, res_line.zinr, "Message Lamp off!", res_line.resnr, res_line.reslinnr))

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
    update_resline()

    return generate_output()