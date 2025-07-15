#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.intevent_1 import intevent_1
from models import Res_line, Messages, Htparam

def messages_init_varbl(if_flag:bool, gastnr:int, resnr:int, reslinnr:int):

    prepare_cache ([Res_line, Messages, Htparam])

    nr = 0
    tot = 0
    mess_list_data = []
    res_line = messages = htparam = None

    mess_list = None

    mess_list_data, Mess_list = create_model("Mess_list", {"nr":int, "mess_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal nr, tot, mess_list_data, res_line, messages, htparam
        nonlocal if_flag, gastnr, resnr, reslinnr


        nonlocal mess_list
        nonlocal mess_list_data

        return {"nr": nr, "tot": tot, "mess-list": mess_list_data}


    mess_list_data.clear()

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
    nr = 0

    for messages in db_session.query(Messages).filter(
             (Messages.gastnr == gastnr) & (Messages.resnr == resnr) & (Messages.reslinnr == reslinnr)).order_by((to_string(get_year(datum)) + to_string(get_month(datum)) + to_string(get_day(datum)) + to_string(zeit))).all():
        mess_list = Mess_list()
        mess_list_data.append(mess_list)

        nr = nr + 1
        mess_list.nr = nr
        mess_list.mess_recid = messages._recid
    tot = nr

    if nr > 1:
        nr = 1

    if tot == 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 310)]})

        if htparam.flogical and if_flag and res_line.active_flag == 1:
            get_output(intevent_1(5, res_line.zinr, "Message Lamp off!", res_line.resnr, res_line.reslinnr))
        pass
        res_line.wabkurz = ""
        pass

    return generate_output()