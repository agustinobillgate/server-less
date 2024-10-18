from functions.additional_functions import *
import decimal
from functions.intevent_1 import intevent_1
from models import Res_line, Messages, Htparam

def messages_init_varbl(if_flag:bool, gastnr:int, resnr:int, reslinnr:int):
    nr = 0
    tot = 0
    mess_list_list = []
    res_line = messages = htparam = None

    mess_list = None

    mess_list_list, Mess_list = create_model("Mess_list", {"nr":int, "mess_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal nr, tot, mess_list_list, res_line, messages, htparam
        nonlocal if_flag, gastnr, resnr, reslinnr


        nonlocal mess_list
        nonlocal mess_list_list
        return {"nr": nr, "tot": tot, "mess-list": mess_list_list}


    mess_list_list.clear()

    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()
    nr = 0

    for messages in db_session.query(Messages).filter(
             (Messages.gastnr == gastnr) & (Messages.resnr == resnr) & (Messages.reslinnr == reslinnr)).order_by((to_string(get_year(datum)) + to_string(get_month(datum)) + to_string(get_day(datum)) + to_string(zeit))).all():
        mess_list = Mess_list()
        mess_list_list.append(mess_list)

        nr = nr + 1
        mess_list.nr = nr
        mess_list.mess_recid = messages._recid
    tot = nr

    if nr > 1:
        nr = 1

    if tot == 0:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 310)).first()

        if htparam.flogical and if_flag and res_line.active_flag == 1:
            get_output(intevent_1(5, res_line.zinr, "Message Lamp off!", res_line.resnr, res_line.reslinnr))
        res_line.wabkurz = ""

    return generate_output()