#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 10/10/2025
# update array: gunakan flag_modified
# Rd, 28/11/2025, with_for_update added
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from functions.intevent_1 import intevent_1
from sqlalchemy.orm.attributes import flag_modified
from models import Res_line, Messages, Bediener, Htparam
from sqlalchemy.orm.attributes import flag_modified

def messages_btn_gobl(rec_id:int, i_case:int, gastnr:int, resnr:int, reslinnr:int, 
                      user_init:string, mess_text_sv:string, caller_sv:string, rufnr_sv:string):

    prepare_cache ([Res_line, Messages, Bediener])

    res_line_zinr = ""
    recid_msg = 0
    res_line = messages = bediener = htparam = None

    db_session = local_storage.db_session
    mess_text_sv = mess_text_sv.strip()
    caller_sv = caller_sv.strip()
    rufnr_sv = rufnr_sv.strip() 

    def generate_output():
        nonlocal res_line_zinr, recid_msg, res_line, messages, bediener, htparam
        nonlocal rec_id, i_case, gastnr, resnr, reslinnr, user_init, mess_text_sv, caller_sv, rufnr_sv
        db_session.commit()
        return {"res_line_zinr": res_line_zinr, "recid_msg": recid_msg}

    def create_messages():

        nonlocal res_line_zinr, recid_msg, res_line, messages, bediener, htparam
        nonlocal rec_id, i_case, gastnr, resnr, reslinnr, user_init, mess_text_sv, caller_sv, rufnr_sv


        messages = Messages()
        

        messages.gastnr = gastnr
        messages.resnr = resnr
        messages.reslinnr = reslinnr
        messages.zeit = get_current_time_in_seconds()

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        messages.usre = bediener.userinit
        messages.zinr = res_line.zinr
        messages.messtext[0] = mess_text_sv
        messages.messtext[1] = caller_sv
        messages.messtext[2] = rufnr_sv
        res_line_zinr = res_line.zinr
        recid_msg = messages._recid
        flag_modified(messages, "messtext")
        db_session.add(messages)
        db_session.commit()
        pass

        htparam = get_cache (Htparam, {"paramnr": [(eq, 310)]})

        if htparam.flogical:

            if res_line.active_flag == 1:
                get_output(intevent_1(4, res_line.zinr, "Message Lamp on!", res_line.resnr, res_line.reslinnr))

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    if i_case == 1:
        create_messages()
    else:
        # messages = get_cache (Messages, {"_recid": [(eq, rec_id)]})
        messages = db_session.query(Messages).filter(Messages._recid == rec_id).with_for_update().first()
        if messages:
            messages.messtext[0] = mess_text_sv
            flag_modified(messages, "messtext")
            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
            messages.usre = bediener.userinit
            flag_modified(messages, "messtext")
            db_session.commit()



    return generate_output()