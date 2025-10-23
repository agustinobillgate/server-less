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
        ct = "$autostart$" + to_string(t_list.autostart) + ";" + #type: ignore
            "$period$" + to_string(t_list.period) + ";" + #type: ignore
            "$delay$" + to_string(t_list.delay) + ";" + #type: ignore
            "$liveflag$" + to_string(t_list.liveflag) + ";" + #type: ignore
            "$defcurr$" + to_string(t_list.defcurr) + ";" + #type: ignore
            "$workpath$" + to_string(t_list.workpath) + ";" + #type: ignore
            "$progname$" + to_string(t_list.progavail) + ";" + #type: ignore
            "$htlcode$" + to_string(t_list.hotelcode) + ";" + #type: ignore
            "$username$" + to_string(lg_token) + ";" + #type: ignore
            "$password$" + to_string(refresh_token) + ";" + #type: ignore
            "$pushrate$" + to_string(t_list.pushrateflag) + ";" + #type: ignore
            "$pullbook$" + to_string(t_list.pullbookflag) + ";" + #type: ignore
            "$pushavail$" + to_string(t_list.pushavailflag) # type: ignore

    queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, bookengid)]})

    if queasy:
        pass
        queasy.char1 = ct
        queasy.date1 = get_current_date()
        pass
        pass

    return generate_output()