#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_bedienerlist_cldbl import read_bedienerlist_cldbl
from functions.pswd_validation_cldbl import pswd_validation_cldbl
from models import Bediener, Htparam

def check_strong_passwordbl(case_type:int, user_name:string, user_pswd:string):

    prepare_cache ([Bediener])

    mess_result = ""
    change_password_flag = False
    bediener_pass:string = ""
    bediener_sha1:string = ""
    bediener = htparam = None

    tp_bediener = shabediener = None

    tp_bediener_data, Tp_bediener = create_model_like(Bediener)

    Shabediener = create_buffer("Shabediener",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, change_password_flag, bediener_pass, bediener_sha1, bediener, htparam
        nonlocal case_type, user_name, user_pswd
        nonlocal shabediener


        nonlocal tp_bediener, shabediener
        nonlocal tp_bediener_data

        return {"mess_result": mess_result, "change_password_flag": change_password_flag}

    def start_vhp():

        nonlocal mess_result, change_password_flag, bediener_pass, bediener_sha1, bediener, htparam
        nonlocal case_type, user_name, user_pswd
        nonlocal shabediener


        nonlocal tp_bediener, shabediener
        nonlocal tp_bediener_data

        nr:int = -1
        pswd_str:string = ""
        pswd_level:int = 0
        pswd_ok:bool = False
        cancel_it:bool = False
        tp_bediener_data = get_output(read_bedienerlist_cldbl(1, user_name))

        tp_bediener = query(tp_bediener_data, first=True)

        if not tp_bediener:
            mess_result = "Login incorrect, please try again."

            return

        if tp_bediener.kassenbest == 1:
            mess_result = "Password Expired!"
            change_password_flag = True

            return
        pswd_ok, pswd_level = get_output(pswd_validation_cldbl(user_name, user_pswd))

        if pswd_ok:
            mess_result = "Password OK!"
            change_password_flag = False

        elif not pswd_ok:
            mess_result = "Your password is not secured enough, It needs to be changed right now!"
            change_password_flag = True

            return


    def check_password():

        nonlocal mess_result, change_password_flag, bediener_pass, bediener_sha1, bediener, htparam
        nonlocal case_type, user_name, user_pswd
        nonlocal shabediener


        nonlocal tp_bediener, shabediener
        nonlocal tp_bediener_data

        nr:int = -1
        pswd_str:string = ""
        pswd_level:int = 0
        pswd_ok:bool = False
        cancel_it:bool = False
        pswd_ok, pswd_level = get_output(pswd_validation_cldbl(user_name, user_pswd))

        if pswd_ok:
            mess_result = "Password OK!"
            change_password_flag = False

        elif not pswd_ok:
            mess_result = "Your password is not secured enough, It needs to be changed right now!"
            change_password_flag = True

            return


    def decode_string1(in_str:string):

        nonlocal mess_result, change_password_flag, bediener_pass, bediener_sha1, bediener, htparam
        nonlocal case_type, user_name, user_pswd
        nonlocal shabediener


        nonlocal tp_bediener, shabediener
        nonlocal tp_bediener_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 71
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)


        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)
        out_str = substring(out_str, 4, (length(out_str) - 4))

        return generate_inner_output()

    change_password_flag = False

    if length(user_pswd) >= 40:

        shabediener = get_cache (Bediener, {"username": [(eq, user_name)]})

        if shabediener:
            bediener_pass = decode_string1(shabediener.usercode)
            bediener_sha1 = sha1(bediener_pass).hexdigest()

            if bediener_sha1.lower()  != (user_pswd).lower() :
                mess_result = "99 - Incorrect Password!"

                return generate_output()
            else:
                user_pswd = bediener_pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 256)]})

    if htparam.flogical :

        if case_type == 1:
            start_vhp()

        elif case_type == 2:
            check_password()
        else:
            mess_result = "Wrong CaseType, please check parameters."

            return generate_output()
    pass

    return generate_output()