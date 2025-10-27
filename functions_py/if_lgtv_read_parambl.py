#using conversion tools version: 1.0.0.117

"""_yusufwijasena_ 10/10/2025

    TICKET ID: 79EBDE
    ISSUE:  - Refactor only
            - add type:ignore to model T_pull_list T_push_list T_list T_lg_list, avoid warning cannot assign attribute 
"""


from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Guest_pr

def if_lgtv_read_parambl(bookengid:int):

    prepare_cache ([Queasy])

    t_pull_list_data = []
    t_push_list_data = []
    t_list_data = []
    t_lg_list_data = []
    i:int = 0
    str:string
    gastnrbe:int = 0
    queasy = guest_pr = None

    t_pull_list = t_push_list = t_list = t_lg_list = None

    t_pull_list_data, T_pull_list = create_model("T_pull_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int})
    t_push_list_data, T_push_list = create_model("T_push_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int})
    t_list_data, T_list = create_model("T_list", {"autostart":bool, "period":int, "delay":int, "hotelcode":string, "username":string, "password":string, "liveflag":bool, "defcurr":string, "pushrateflag":bool, "pullbookflag":bool, "pushavailflag":bool, "workpath":string, "progavail":string, "tokencreated":date})
    t_lg_list_data, T_lg_list = create_model("T_lg_list", {"vcwsagent":string, "client_id":string, "client_secret":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_pull_list_data, t_push_list_data, t_list_data, t_lg_list_data, i, str, gastnrbe, queasy, guest_pr
        nonlocal bookengid


        nonlocal t_pull_list, t_push_list, t_list, t_lg_list
        nonlocal t_pull_list_data, t_push_list_data, t_list_data, t_lg_list_data

        return {"t-pull-list": t_pull_list_data, "t-push-list": t_push_list_data, "t-list": t_list_data, "t-lg-list": t_lg_list_data}


    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, bookengid)]})

    if queasy:
        gastnrbe = queasy.number2

    queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, bookengid)]})

    if queasy:
        t_list = T_list()
        t_list_data.append(t_list)

        for i in range(1,num_entries(queasy.char1, ";")  + 1) :  #type: ignore
            str = entry(i - 1, queasy.char1, ";")  #type: ignore

            if substring(str, 0, 11) == ("$autostart$").lower() :  #type: ignore
                t_list.autostart = logical(substring(str, 11))  #type: ignore

            elif substring(str, 0, 8) == ("$period$").lower() :  #type: ignore
                t_list.period = to_int(substring(str, 8))  #type: ignore

            elif substring(str, 0, 7) == ("$delay$").lower() :  #type: ignore
                t_list.delay = to_int(substring(str, 7))  #type: ignore

            elif substring(str, 0, 10) == ("$liveflag$").lower() :  #type: ignore
                t_list.liveflag = logical(substring(str, 10))  #type: ignore

            elif substring(str, 0, 9) == ("$defcurr$").lower() :  #type: ignore
                t_list.defcurr = substring(str, 9)  #type: ignore

            elif substring(str, 0, 10) == ("$workpath$").lower() :  #type: ignore
                t_list.workpath = substring(str, 10)  #type: ignore

            elif substring(str, 0, 10) == ("$progname$").lower() :  #type: ignore
                t_list.progavail = substring(str, 10)  #type: ignore
            elif substring(str, 0, 9) == ("$htlcode$").lower() :  #type: ignore
                t_list.hotelcode = substring(str, 9)  #type: ignore

            elif substring(str, 0, 10) == ("$username$").lower() :  #type: ignore
                t_list.username = substring(str, 10)  #type: ignore

            elif substring(str, 0, 10) == ("$password$").lower() :  #type: ignore
                t_list.password = substring(str, 10)  #type: ignore

            elif substring(str, 0, 10) == ("$pushrate$").lower() :  #type: ignore
                t_list.pushrateflag = logical(substring(str, 10))  #type: ignore

            elif substring(str, 0, 10) == ("$pullbook$").lower() :  #type: ignore
                t_list.pullbookflag = logical(substring(str, 10))  #type: ignore

            elif substring(str, 0, 11) == ("$pushavail$").lower() :  #type: ignore
                t_list.pushavailflag = logical(substring(str, 11))  #type: ignore
        t_list.tokencreated = queasy.date1  # type: ignore

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 163) & (Queasy.number1 == bookengid)).order_by(Queasy._recid).all():
        t_pull_list = T_pull_list()
        t_pull_list_data.append(t_pull_list)

        t_pull_list.rcodevhp = entry(0, queasy.char1, ";") #type: ignore 
        t_pull_list.rcodebe = entry(1, queasy.char1, ";") #type: ignore
        t_pull_list.rmtypevhp = entry(2, queasy.char1, ";") #type: ignore
        t_pull_list.rmtypebe = entry(3, queasy.char1, ";") #type: ignore
        t_pull_list.argtvhp = entry(4, queasy.char1, ";") #type: ignore

    queasy_obj_list = {}
    for queasy, guest_pr in db_session.query(Queasy, Guest_pr).join(Guest_pr,(Guest_pr.gastnr == gastnrbe) & (Guest_pr.code == entry(0, Queasy.char1, ";"))).filter(
             (Queasy.key == 161) & (Queasy.number1 == bookengid)).order_by(Queasy._recid).all():
        if queasy_obj_list.get(queasy._recid):
            continue
        else:
            queasy_obj_list[queasy._recid] = True


        t_push_list = T_push_list()
        t_push_list_data.append(t_push_list)

        t_push_list.rcodevhp = entry(0, queasy.char1, ";") #type: ignore
        t_push_list.rcodebe = entry(1, queasy.char1, ";") #type: ignore
        t_push_list.rmtypevhp = entry(2, queasy.char1, ";") #type: ignore
        t_push_list.rmtypebe = entry(3, queasy.char1, ";") #type: ignore
        t_push_list.argtvhp = entry(4, queasy.char1, ";") #type: ignore

    queasy = get_cache (Queasy, {"key": [(eq, 306)],"char1": [(ne, "")],"char2": [(ne, "")]})

    if queasy:
        t_lg_list = T_lg_list()
        t_lg_list_data.append(t_lg_list)

        t_lg_list.vcwsagent = queasy.char2  # type: ignore


        t_lg_list.client_id = entry(0, queasy.char1, "|")  # type: ignore
        t_lg_list.client_secret = entry(1, queasy.char1, "|") # type: ignore

    return generate_output()