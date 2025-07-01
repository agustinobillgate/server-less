#using conversion tools version: 1.0.0.111

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
    t_messages_list = []
    mess_list_list = []
    mess_data_list = []
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

    mess_list_list, Mess_list = create_model("Mess_list", {"nr":int, "mess_recid":int})
    t_messages_list, T_messages = create_model_like(Messages, {"rec_id":int})
    mess_data_list, Mess_data = create_model("Mess_data", {"gname":string, "arrival":date, "depart":date, "zinr":string, "pguest":bool, "nr":int, "tot":int, "username":string, "messtext":string, "currtime":string, "caller":string, "phoneno":string, "currdate":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal v_success, t_messages_list, mess_list_list, mess_data_list, gname, arrival, depart, zinr, pguest, nr, tot, num, username, mess_text, curr_time, caller, rufnr, curr_date, messages
        nonlocal gastnr, resnr, reslinnr, v_key, v_deactive


        nonlocal mess_list, t_messages, mess_data
        nonlocal mess_list_list, t_messages_list, mess_data_list

        return {"v_success": v_success, "t-messages": t_messages_list, "mess-list": mess_list_list, "mess-data": mess_data_list}

    def init_var(if_flag:bool):

        nonlocal v_success, t_messages_list, mess_list_list, mess_data_list, gname, arrival, depart, zinr, pguest, nr, tot, num, username, mess_text, curr_time, caller, rufnr, curr_date, messages
        nonlocal gastnr, resnr, reslinnr, v_key, v_deactive


        nonlocal mess_list, t_messages, mess_data
        nonlocal mess_list_list, t_messages_list, mess_data_list


        nr, tot, mess_list_list = get_output(messages_init_varbl(if_flag, gastnr, resnr, reslinnr))
        mess_text = ""
        curr_date = None
        curr_time = ""
        username = ""
        caller = ""
        rufnr = ""

        if v_key.lower()  == ("FIRST").lower() :
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

        nonlocal v_success, t_messages_list, mess_list_list, mess_data_list, gname, arrival, depart, zinr, pguest, nr, tot, num, username, mess_text, curr_time, caller, rufnr, curr_date, messages
        nonlocal gastnr, resnr, reslinnr, v_key, v_deactive


        nonlocal mess_list, t_messages, mess_data
        nonlocal mess_list_list, t_messages_list, mess_data_list

        if i < 1:

            return

        elif i > tot:

            return

        elif tot == 0:

            return
        else:
            nr = i

            mess_list = query(mess_list_list, filters=(lambda mess_list: mess_list.nr == i), first=True)
            username, t_messages_list = get_output(messages_get_messagebl(mess_list.mess_recid))

            t_messages = query(t_messages_list, first=True)
            mess_text = t_messages.messtext[0]
            caller = t_messages.messtext[1]
            rufnr = t_messages.messtext[2]
            curr_date = t_messages.datum
            curr_time = to_string(t_messages.zeit, "HH:MM:SS")

    gname, arrival, depart, zinr, pguest = get_output(prepare_messagesbl(gastnr, resnr, reslinnr))

    if v_key.lower()  == ("DEL").lower()  or v_key.lower()  == ("DEACTIVE").lower() :
        init_var(True)

        if v_deactive:
            get_output(messages_update_reslinebl(t_messages.resnr, t_messages.reslinnr))
    else:
        init_var(False)
    mess_data = Mess_data()
    mess_data_list.append(mess_data)

    mess_data.gname = gname
    mess_data.arrival = arrival
    mess_data.depart = depart
    mess_data.zinr = zinr
    mess_data.pguest = pguest
    mess_data.nr = nr
    mess_data.tot = tot
    mess_data.username = username
    mess_data.messtext = mess_text
    mess_data.currtime = curr_time
    mess_data.caller = caller
    mess_data.phoneno = rufnr
    mess_data.currdate = curr_date

    return generate_output()