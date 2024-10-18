from functions.additional_functions import *
import decimal
from functions.intevent_1 import intevent_1
from models import Messages, Res_line, Htparam

def messages_btn_messbl(t_messages_resnr:int, t_messages_reslinnr:int, rec_id:int):
    messages = res_line = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal messages, res_line, htparam
        nonlocal t_messages_resnr, t_messages_reslinnr, rec_id


        return {}


    messages = db_session.query(Messages).filter(
                 (Messages._recid == rec_id)).first()

    if messages:
        messages.betriebsnr = 1

    res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == t_messages_resnr) & (Res_line.reslinnr == t_messages_reslinnr)).first()

    htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 310)).first()

    if htparam.flogical and res_line.active_flag == 1:
        get_output(intevent_1(5, res_line.zinr, "Message Lamp off!", res_line.resnr, res_line.reslinnr))
    res_line.wabkurz = ""


    return generate_output()