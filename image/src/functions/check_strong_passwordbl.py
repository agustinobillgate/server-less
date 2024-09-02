from functions.additional_functions import *
import decimal
from functions.read_bedienerlist_cldbl import read_bedienerlist_cldbl
from functions.pswd_validation_cldbl import pswd_validation_cldbl
from models import Bediener, Htparam

def check_strong_passwordbl(case_type:int, user_name:str, user_pswd:str):
    print("U/P/C:", user_name, user_pswd, case_type)
    mess_result = ""
    change_password_flag = False
    bediener = htparam = None
    tp_bediener = None
    tp_bediener_list, Tp_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, change_password_flag, bediener, htparam
        nonlocal case_type, user_name, user_pswd


        nonlocal tp_bediener
        nonlocal tp_bediener_list
        return {"mess_result": mess_result, "change_password_flag": change_password_flag}

    def start_vhp():
        nonlocal mess_result, change_password_flag, bediener, htparam
        nonlocal case_type, user_name, user_pswd
        nonlocal tp_bediener
        nonlocal tp_bediener_list
        print("Masuk startVHP")
        nr:int = -1
        pswd_str:str = ""
        pswd_level:int = 0
        pswd_ok:bool = False
        cancel_it:bool = False
        tp_bediener_list = get_output(read_bedienerlist_cldbl(1, user_name))
        print("Read_bediener ->", len(tp_bediener_list), tp_bediener_list)

        if not tp_bediener_list:
            tp_bediener = query(tp_bediener_list, first=True)
            print("TP:", tp_bediener)

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
        nonlocal mess_result, change_password_flag, bediener, htparam
        nonlocal case_type, user_name, user_pswd
        nonlocal tp_bediener
        nonlocal tp_bediener_list

        nr:int = -1
        pswd_str:str = ""
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

    change_password_flag = False
    print("Check Param 256.")
    htparam = db_session.query(Htparam).filter((Htparam.paramnr == 256)).first()    
    if htparam:
        print("ada 256:", case_type)
        if htparam.flogical :
            if case_type == 1:
                print("Masuk start_vhp")
                start_vhp()
            elif case_type == 2:
                print("Masuk check_password")
                check_password()
            else:
                mess_result = "Wrong CaseType, please check parameters."
                return generate_output()
    else:
        print("tidak ada Param 256")

    return generate_output()