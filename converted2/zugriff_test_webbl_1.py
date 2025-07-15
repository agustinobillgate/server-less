from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, Messages, Paramtext

value_list_list, Value_list = create_model("Value_list", {"var_name":str, "value_str":str})

def zugriff_test_webbl(user_init:str, array_nr:int, expected_nr:int):
    zugriff = True
    epoch_signature = 0
    mess_str = ""
    signature_list_list = []
    mail_exist:bool = False
    logical_flag:bool = False
    n:int = 0
    perm:List[int] = create_empty_list(120,0)
    s1:str = ""
    s2:str = ""
    mn_date:date = None
    anz:int = 0
    username:str = ""
    bediener = messages = paramtext = None

    value_list = signature_list = tp_bediener = t_messages = None

    signature_list_list, Signature_list = create_model("Signature_list", {"var_name":str, "signature":str})
    tp_bediener_list, Tp_bediener = create_model_like(Bediener)
    t_messages_list, T_messages = create_model_like(Messages)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal zugriff, epoch_signature, mess_str, signature_list_list, mail_exist, logical_flag, n, perm, s1, s2, mn_date, anz, username, bediener, messages, paramtext
        nonlocal user_init, array_nr, expected_nr
        global value_list_list

        nonlocal value_list, signature_list, tp_bediener, t_messages
        nonlocal  signature_list_list, tp_bediener_list, t_messages_list
        return {"zugriff": zugriff, "epoch_signature": epoch_signature, "mess_str": mess_str, "signature-list": signature_list_list}

    def create_signature(user_name:str, value_list_list:[Value_list]):

        nonlocal zugriff, epoch_signature, mess_str, signature_list_list, mail_exist, logical_flag, n, perm, s1, s2, mn_date, anz, username, bediener, messages, paramtext
        nonlocal user_init, array_nr, expected_nr


        nonlocal value_list, signature_list, tp_bediener, t_messages
        nonlocal signature_list_list, tp_bediener_list, t_messages_list

        epoch = 0
        dtz1 = None
        dtz2 = None
        lic_nr:str = ""
        data:str = ""
        value_str:str = ""

        def generate_inner_output():
            return (epoch, signature_list)


        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == 243)).first()

        if paramtext and paramtext.ptexte != "":
            lic_nr = decode_string(paramtext.ptexte)
        dtz1 = get_current_datetime()
        dtz2 = parse("1970-01-01T00:00:00.000+0:00")
        epoch = get_interval(dtz1, dtz2, "milliseconds")

        for value_list in query(value_list_list):
            value_str = value_list.value_str.lower()

            if value_str == "yes":
                value_str = "true"
            elif value_str == "no":
                value_str = "false"
            data = value_str + "-" + to_string(epoch) + "-" + to_string(lic_nr) + "-" + user_name.lower()
            signature_list = Signature_list()
            signature_list_list.append(signature_list)

            signature_list.var_name = value_list.var_name
            signature_list.signature = sha1(data).hexdigest()

        return generate_inner_output()


    def decode_string(in_str:str):

        nonlocal zugriff, epoch_signature, mess_str, signature_list_list, mail_exist, logical_flag, n, perm, s1, s2, mn_date, anz, username, bediener, messages, paramtext
        nonlocal user_init, array_nr, expected_nr
        global value_list_list

        nonlocal value_list, signature_list, tp_bediener, t_messages
        nonlocal signature_list_list, tp_bediener_list, t_messages_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    if user_init == "":
        zugriff = False
        mess_str = "User not defined."

        return generate_output()
    else:

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            tp_bediener = Tp_bediener()
            tp_bediener_list.append(tp_bediener)

            buffer_copy(bediener, tp_bediener)
            username = bediener.username
        else:
            zugriff = False
            mess_str = "User not found."

            return generate_output()
        for n in range(1,len(tp_bediener.permissions)  + 1) :
            perm[n - 1] = to_int(substring(tp_bediener.permissions, n - 1, 1))

        if perm[array_nr - 1] < expected_nr:
            zugriff = False
            s1 = to_string(array_nr, "999")
            s2 = to_string(expected_nr)
            mess_str = "Sorry, No Access Right, Access Code = " + s1 + s2
        value_list = Value_list()
        value_list_list.append(value_list)

        value_list.var_name = "zugriff"
        value_list.value_str = to_string(zugriff)


        epoch_signature, signature_list_list = create_signature(username, value_list_list)

    return generate_output()