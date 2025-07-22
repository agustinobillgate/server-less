#using conversion tools version: 1.0.0.117
# ----------------------------------------
# Rd, 22/7/2025
# Add eliminate None
# ----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Messages

def zugriff_test(user_init:string, array_nr:int, expected_nr:int):
    zugriff = True
    mess_str = ""
    mail_exist:bool = False
    logical_flag:bool = False
    n:int = 0
    perm:List[int] = create_empty_list(99,0)
    s1:string = ""
    s2:string = ""
    mn_date:date = None
    anz:int = 0
    bediener = messages = None

    tp_bediener = t_messages = None

    tp_bediener_data, Tp_bediener = create_model_like(Bediener)
    t_messages_data, T_messages = create_model_like(Messages)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal zugriff, mess_str, mail_exist, logical_flag, n, perm, s1, s2, mn_date, anz, bediener, messages
        nonlocal user_init, array_nr, expected_nr


        nonlocal tp_bediener, t_messages
        nonlocal tp_bediener_data, t_messages_data

        return {"zugriff": zugriff, "mess_str": mess_str}


    if user_init == "":
        zugriff = False
        mess_str = "User not defined."

        return generate_output()
    else:

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            tp_bediener = Tp_bediener()
            tp_bediener_data.append(tp_bediener)

            buffer_copy(bediener, tp_bediener)

            # Rd 22/7/2025 (AI)
            # eliminate None
            if tp_bediener.permissions is None:
                zugriff = False
                mess_str = "User has no permissions assigned."
                return generate_output()
            perm = []
            for n in range(1, length(tp_bediener.permissions) + 1):
                perm.append(to_int(substring(tp_bediener.permissions, n - 1, 1)))

            if perm[array_nr - 1] < expected_nr:
                zugriff = False
                s1 = to_string(array_nr, "99")
                s2 = to_string(expected_nr)
                mess_str = "Sorry, No Access Right, Access Code = " + s1 + s2
        else:
            zugriff = False
            mess_str = "User not found."

            return generate_output()
        
        for n in range(1,length(tp_bediener.permissions)  + 1) :
            perm[n - 1] = to_int(substring(tp_bediener.permissions, n - 1, 1))

        if perm[array_nr - 1] < expected_nr:
            zugriff = False
            s1 = to_string(array_nr, "99")
            s2 = to_string(expected_nr)
            mess_str = "Sorry, No Access Right, Access Code = " + s1 + s2

    return generate_output()