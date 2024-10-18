from functions.additional_functions import *
import decimal
from functions.intevent_1 import intevent_1
from models import Res_line, Messages

def messages_update_reslinebl(resnr:int, reslinnr:int):
    res_line = messages = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line, messages
        nonlocal resnr, reslinnr


        return {}

    def update_resline():

        nonlocal res_line, messages
        nonlocal resnr, reslinnr

        messages = db_session.query(Messages).filter(
                 (Messages.resnr == resnr) & (Messages.reslinnr == reslinnr) & (Messages.betriebsnr == 0)).first()

        if messages:

            if res_line.wabkurz == "":
                res_line.wabkurz = "M"

                if res_line.active_flag == 1:
                    get_output(intevent_1(4, res_line.zinr, "Message Lamp on!", res_line.resnr, res_line.reslinnr))
        else:

            if res_line.wabkurz.lower()  == ("M").lower() :
                res_line.wabkurz = ""

                if res_line.active_flag == 1:
                    get_output(intevent_1(5, res_line.zinr, "Message Lamp off!", res_line.resnr, res_line.reslinnr))

    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()
    update_resline()

    return generate_output()