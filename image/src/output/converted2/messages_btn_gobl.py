from functions.additional_functions import *
import decimal
from sqlalchemy import func
from functions.intevent_1 import intevent_1
from models import Res_line, Messages, Bediener, Htparam

def messages_btn_gobl(rec_id:int, i_case:int, gastnr:int, resnr:int, reslinnr:int, user_init:str, mess_text_sv:str, caller_sv:str, rufnr_sv:str):
    res_line_zinr = ""
    recid_msg = 0
    res_line = messages = bediener = htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line_zinr, recid_msg, res_line, messages, bediener, htparam
        nonlocal rec_id, i_case, gastnr, resnr, reslinnr, user_init, mess_text_sv, caller_sv, rufnr_sv


        return {"res_line_zinr": res_line_zinr, "recid_msg": recid_msg}

    def create_messages():

        nonlocal res_line_zinr, recid_msg, res_line, messages, bediener, htparam
        nonlocal rec_id, i_case, gastnr, resnr, reslinnr, user_init, mess_text_sv, caller_sv, rufnr_sv


        messages = Messages()
        db_session.add(messages)

        messages.gastnr = gastnr
        messages.resnr = resnr
        messages.reslinnr = reslinnr
        messages.zeit = get_current_time_in_seconds()

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()
        messages.usre = bediener.userinit
        messages.zinr = res_line.zinr
        messages.messtext[0] = mess_text_sv
        messages.messtext[1] = caller_sv
        messages.messtext[2] = rufnr_sv
        res_line_zinr = res_line.zinr
        recid_msg = messages._recid

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 310)).first()

        if htparam.flogical:

            if res_line.active_flag == 1:
                get_output(intevent_1(4, res_line.zinr, "Message Lamp on!", res_line.resnr, res_line.reslinnr))

    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()

    if i_case == 1:
        create_messages()
    else:

        messages = db_session.query(Messages).filter(
                 (Messages._recid == rec_id)).first()
        messages.messtext[0] = mess_text_sv

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()
        messages.usre = bediener.userinit

    return generate_output()