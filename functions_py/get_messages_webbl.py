#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 10/10/2025
# message kosong
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_messagesbl import prepare_messagesbl
from functions.messages_update_reslinebl import messages_update_reslinebl
from functions.messages_init_varbl import messages_init_varbl
from functions.messages_get_messagebl import messages_get_messagebl
from models import Messages

def get_messages_webbl(gastnr:int, resnr:int, reslinnr:int, v_key:string, v_deactive:bool):
    v_success = False
    t_messages_data = []
    mess_list_data = []
    mess_data_data = []
    gname:string = ""
    arrival:date = None
    depart:date = None
    zinr:string = ""
    pguest:bool = False
    nr:int = 0
    tot:int = 0
    num:int = 0
    username:string = ""
    mess_text:string = ""
    curr_time:string = ""
    caller:string = ""
    rufnr:string = ""
    curr_date:date = None
    messages = None

    mess_list = t_messages = mess_data = None

    mess_list_data, Mess_list = create_model("Mess_list", {"nr":int, "mess_recid":int})
    t_messages_data, T_messages = create_model_like(Messages, {"rec_id":int})
    mess_data_data, Mess_data = create_model("Mess_data", {"gname":string, "arrival":date, "depart":date, "zinr":string, "pguest":bool, "nr":int, "tot":int, "username":string, "messText":string, "currTime":string, "caller":string, "phoneNo":string, "currDate":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal v_success, t_messages_data, mess_list_data, mess_data_data, gname, arrival, depart, zinr, pguest, nr, tot, num, username, mess_text, curr_time, caller, rufnr, curr_date, messages
        nonlocal gastnr, resnr, reslinnr, v_key, v_deactive


        nonlocal mess_list, t_messages, mess_data
        nonlocal mess_list_data, t_messages_data, mess_data_data

        return {"v_success": v_success, "t-messages": t_messages_data, "mess-list": mess_list_data, "mess-data": mess_data_data}

    def init_var(if_flag:bool):

        nonlocal v_success, t_messages_data, mess_list_data, mess_data_data, gname, arrival, depart, zinr, pguest, nr, tot, num, username, mess_text, curr_time, caller, rufnr, curr_date, messages
        nonlocal gastnr, resnr, reslinnr, v_key, v_deactive
        nonlocal mess_list, t_messages, mess_data
        nonlocal mess_list_data, t_messages_data, mess_data_data
        nr, tot, mess_list_data = get_output(messages_init_varbl(if_flag, gastnr, resnr, reslinnr))
        mess_text = ""
        curr_date = None
        curr_time = ""
        username = ""
        caller = ""
        rufnr = ""

        if v_key  == ("FIRST") :
            get_messages(1)
            nr = 1

        elif matches(v_key,r"*NEXT*"):
            num = to_int(substring(v_key, 4))
            get_messages(num + 1)
            nr = num + 1

        elif matches(v_key,r"*PREV*"):
            num = to_int(substring(v_key, 4))
            get_messages(num - 1)
            nr = num - 1

        elif matches(v_key,r"*DEACTIVE*"):
            num = to_int(substring(v_key, 8))
            get_messages(num)
        else:
            get_messages(nr)


    def get_messages(i:int):

        nonlocal v_success, t_messages_data, mess_list_data, mess_data_data, gname, arrival, depart, zinr, pguest, nr, tot, num, username, mess_text, curr_time, caller, rufnr, curr_date, messages
        nonlocal gastnr, resnr, reslinnr, v_key, v_deactive


        nonlocal mess_list, t_messages, mess_data
        nonlocal mess_list_data, t_messages_data, mess_data_data

        if i < 1:

            return

        elif i > tot:

            return

        elif tot == 0:

            return
        else:
            nr = i

            mess_list = query(mess_list_data, filters=(lambda mess_list: mess_list.nr == i), first=True)
            username, t_messages_data = get_output(messages_get_messagebl(mess_list.mess_recid))

            # t_messages = query(t_messages_data, first=True)
            for t_messages in t_messages_data:
                mess_text = t_messages.messtext[0]
                caller = t_messages.messtext[1]
                rufnr = t_messages.messtext[2]
                curr_date = t_messages.datum
                curr_time = to_string(t_messages.zeit, "HH:MM:SS")

    gname, arrival, depart, zinr, pguest = get_output(prepare_messagesbl(gastnr, resnr, reslinnr))

    if v_key  == ("DEL")  or v_key  == ("DEACTIVE") :
        init_var(True)

        if v_deactive:
            get_output(messages_update_reslinebl(t_messages.resnr, t_messages.reslinnr))
    else:
        init_var(False)
    mess_data = Mess_data()
    mess_data_data.append(mess_data)

    mess_data.gname = gname
    mess_data.arrival = arrival
    mess_data.depart = depart
    mess_data.zinr = zinr
    mess_data.pguest = pguest
    mess_data.nr = nr
    mess_data.tot = tot
    mess_data.username = username
    mess_data.messText = mess_text
    mess_data.currTime = curr_time
    mess_data.caller = caller
    mess_data.phoneNo = rufnr
    mess_data.currDate = curr_date

    return generate_output()