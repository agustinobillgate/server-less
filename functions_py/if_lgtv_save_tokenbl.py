#using conversion tools version: 1.0.0.117

"""_yusufwijasena_ 10/10/2025

    TICKET ID: 79EBDE
    ISSUE:  - Refactor only
            - add type:ignore to model T_list, avoid warning cannot assign attribute
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy

t_list_data, T_list = create_model("T_list", {"autostart":bool, "period":int, "delay":int, "hotelcode":string, "username":string, "password":string, "liveflag":bool, "defcurr":string, "pushrateflag":bool, "pullbookflag":bool, "pushavailflag":bool, "workpath":string, "progavail":string, "tokencreated":date})

def if_lgtv_save_tokenbl(bookengid:int, lg_token:string, refresh_token:string, t_list_data:[T_list]): # type: ignore

    prepare_cache ([Queasy])

    ct:str = ""
    number1:int = 0
    queasy = None

    t_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ct, number1, queasy
        nonlocal bookengid, lg_token, refresh_token


        nonlocal t_list

        return {"ct": ct}

    t_list = query(t_list_data, first=True)

    if t_list:
        ct = "$autostart$" + to_string(t_list.autostart) + ";" +\
            "$period$" + to_string(t_list.period) + ";" +\
            "$delay$" + to_string(t_list.delay) + ";" +\
            "$liveflag$" + to_string(t_list.liveflag) + ";" +\
            "$defcurr$" + to_string(t_list.defcurr) + ";" +\
            "$workpath$" + to_string(t_list.workpath) + ";" +\
            "$progname$" + to_string(t_list.progavail) + ";" +\
            "$htlcode$" + to_string(t_list.hotelcode) + ";" +\
            "$username$" + to_string(lg_token) + ";" +\
            "$password$" + to_string(refresh_token) + ";" +\
            "$pushrate$" + to_string(t_list.pushrateflag) + ";" +\
            "$pullbook$" + to_string(t_list.pullbookflag) + ";" +\
            "$pushavail$" + to_string(t_list.pushavailflag) 

    queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, bookengid)]})

    if queasy:
        pass
        queasy.char1 = ct
        queasy.date1 = get_current_date()
        pass
        pass

    return generate_output()