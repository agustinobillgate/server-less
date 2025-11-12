#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Guest_pr

def if_siteminder_read_parambl(bookengid:int):

    prepare_cache ([Queasy])

    t_pull_list_data = []
    t_push_list_data = []
    t_list_data = []
    i:int = 0
    str:string = ""
    gastnrbe:int = 0
    queasy = guest_pr = None

    t_pull_list = t_push_list = t_list = None

    t_pull_list_data, T_pull_list = create_model("T_pull_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int})
    t_push_list_data, T_push_list = create_model("T_push_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int})
    t_list_data, T_list = create_model("T_list", {"autostart":bool, "period":int, "delay":int, "hotelcode":string, "username":string, "password":string, "liveflag":bool, "defcurr":string, "pushrateflag":bool, "pullbookflag":bool, "pushavailflag":bool, "workpath":string, "progavail":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_pull_list_data, t_push_list_data, t_list_data, i, str, gastnrbe, queasy, guest_pr
        nonlocal bookengid


        nonlocal t_pull_list, t_push_list, t_list
        nonlocal t_pull_list_data, t_push_list_data, t_list_data

        return {"t-pull-list": t_pull_list_data, "t-push-list": t_push_list_data, "t-list": t_list_data}

    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, bookengid)]})

    if queasy:
        gastnrbe = queasy.number2

    queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, bookengid)]})

    if queasy:
        t_list = T_list()
        t_list_data.append(t_list)

        for i in range(1,num_entries(queasy.char1, ";")  + 1) :
            str = entry(i - 1, queasy.char1, ";")

            if substring(str, 0, 11) == ("$autostart$").lower() :
                t_list.autostart = logical(substring(str, 11))

            elif substring(str, 0, 8) == ("$period$").lower() :
                t_list.period = to_int(substring(str, 8))

            elif substring(str, 0, 7) == ("$delay$").lower() :
                t_list.delay = to_int(substring(str, 7))

            elif substring(str, 0, 10) == ("$liveflag$").lower() :
                t_list.liveflag = logical(substring(str, 10))

            elif substring(str, 0, 9) == ("$defcurr$").lower() :
                t_list.defcurr = substring(str, 9)

            elif substring(str, 0, 10) == ("$workpath$").lower() :
                t_list.workpath = substring(str, 10)

            elif substring(str, 0, 10) == ("$progname$").lower() :
                t_list.progavail = substring(str, 10)

            elif substring(str, 0, 9) == ("$htlcode$").lower() :
                t_list.hotelcode = substring(str, 9)

            elif substring(str, 0, 10) == ("$username$").lower() :
                t_list.username = substring(str, 10)

            elif substring(str, 0, 10) == ("$password$").lower() :
                t_list.password = substring(str, 10)

            elif substring(str, 0, 10) == ("$pushrate$").lower() :
                t_list.pushrateflag = logical(substring(str, 10))

            elif substring(str, 0, 10) == ("$pullbook$").lower() :
                t_list.pullbookflag = logical(substring(str, 10))

            elif substring(str, 0, 11) == ("$pushavail$").lower() :
                t_list.pushavailflag = logical(substring(str, 11))

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 163) & (Queasy.number1 == bookengid)).order_by(Queasy._recid).all():
        t_pull_list = T_pull_list()
        t_pull_list_data.append(t_pull_list)

        t_pull_list.rcodevhp = entry(0, queasy.char1, ";")
        t_pull_list.rcodebe = entry(1, queasy.char1, ";")
        t_pull_list.rmtypevhp = entry(2, queasy.char1, ";")
        t_pull_list.rmtypebe = entry(3, queasy.char1, ";")
        t_pull_list.argtvhp = entry(4, queasy.char1, ";")

    queasy_obj_list = {}
    for queasy, guest_pr in db_session.query(Queasy, Guest_pr).join(Guest_pr,(Guest_pr.gastnr == gastnrbe) & (Guest_pr.code == entry(0, Queasy.char1, ";"))).filter(
             (Queasy.key == 161) & (Queasy.number1 == bookengid)).order_by(Queasy._recid).all():
        if queasy_obj_list.get(queasy._recid):
            continue
        else:
            queasy_obj_list[queasy._recid] = True


        t_push_list = T_push_list()
        t_push_list_data.append(t_push_list)

        t_push_list.rcodevhp = entry(0, queasy.char1, ";")
        t_push_list.rcodebe = entry(1, queasy.char1, ";")
        t_push_list.rmtypevhp = entry(2, queasy.char1, ";")
        t_push_list.rmtypebe = entry(3, queasy.char1, ";")
        t_push_list.argtvhp = entry(4, queasy.char1, ";")

    return generate_output()

