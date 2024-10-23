from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Bediener

def get_bediener_infobl(user_name:str, user_init:str):
    bediener_info_list = []
    queasy = bediener = None

    bediener_info = buser = bdept = None

    bediener_info_list, Bediener_info = create_model("Bediener_info", {"user_number":int, "user_init":str, "user_name":str, "dept_number":int, "dept_name":str, "email":str, "mobile":str, "pager":str})

    Buser = create_buffer("Buser",Queasy)
    Bdept = create_buffer("Bdept",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bediener_info_list, queasy, bediener
        nonlocal user_name, user_init
        nonlocal buser, bdept


        nonlocal bediener_info, buser, bdept
        nonlocal bediener_info_list
        return {"bediener-info": bediener_info_list}

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower()) & (func.lower(Bediener.username) == (user_name).lower())).first()

    if bediener:

        buser = db_session.query(Buser).filter(
                 (Buser.key == 134) & (Buser.number1 == bediener.nr) & (Buser.betriebsnr == 0) & (Buser.deci1 == 0) & (Buser.logi1 == False)).first()

        bdept = db_session.query(Bdept).filter(
                 (Bdept.key == 19) & (Bdept.number1 == bediener.user_group)).first()
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

    return generate_output()