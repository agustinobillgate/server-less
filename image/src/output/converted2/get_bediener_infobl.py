#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener

def get_bediener_infobl(user_name:string, user_init:string):

    prepare_cache ([Queasy, Bediener])

    bediener_info_list = []
    queasy = bediener = None

    bediener_info = buser = bdept = totpdata = None

    bediener_info_list, Bediener_info = create_model("Bediener_info", {"user_number":int, "user_init":string, "user_name":string, "dept_number":int, "dept_name":string, "email":string, "mobile":string, "pager":string, "totp_flag":bool, "totp_status":string})

    Buser = create_buffer("Buser",Queasy)
    Bdept = create_buffer("Bdept",Queasy)
    Totpdata = create_buffer("Totpdata",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bediener_info_list, queasy, bediener
        nonlocal user_name, user_init
        nonlocal buser, bdept, totpdata


        nonlocal bediener_info, buser, bdept, totpdata
        nonlocal bediener_info_list

        return {"bediener-info": bediener_info_list}

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)],"username": [(eq, user_name)]})

    if bediener:

        buser = get_cache (Queasy, {"key": [(eq, 134)],"number1": [(eq, bediener.nr)],"betriebsnr": [(eq, 0)],"deci1": [(eq, 0)],"logi1": [(eq, False)]})

        bdept = get_cache (Queasy, {"key": [(eq, 19)],"number1": [(eq, bediener.user_group)]})
        bediener_info = Bediener_info()
        bediener_info_list.append(bediener_info)

        bediener_info.user_number = bediener.nr
        bediener_info.user_init = bediener.userinit
        bediener_info.user_name = bediener.username
        bediener_info.dept_number = bediener.user_group
        bediener_info.dept_name = bdept.char3
        bediener_info.email = buser.char2
        bediener_info.mobile = buser.char1
        bediener_info.pager = buser.char3

        totpdata = get_cache (Queasy, {"key": [(eq, 314)],"char1": [(eq, bediener.username)]})

        if totpdata:
            bediener_info.totp_flag = True

            if totpdata.logi1 :
                bediener_info.totp_status = "ACTIVE"
            else:
                bediener_info.totp_status = "INACTIVE"

            return generate_output()

    return generate_output()