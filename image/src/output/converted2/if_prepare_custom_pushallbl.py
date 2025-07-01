#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam

def if_prepare_custom_pushallbl(becode:int):

    prepare_cache ([Queasy, Htparam])

    t_list_list = []
    t_push_list_list = []
    date_110 = None
    i:int = 0
    str:string = ""
    queasy = htparam = None

    t_list = t_push_list = None

    t_list_list, T_list = create_model("T_list", {"progavail":string, "hotelcode":string, "pushrate_flag":bool, "pushavail_flag":bool, "period":int})
    t_push_list_list, T_push_list = create_model("T_push_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int, "license":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_list_list, t_push_list_list, date_110, i, str, queasy, htparam
        nonlocal becode


        nonlocal t_list, t_push_list
        nonlocal t_list_list, t_push_list_list

        return {"t-list": t_list_list, "t-push-list": t_push_list_list, "date_110": date_110}


    queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, becode)]})

    if queasy:
        t_list = T_list()
        t_list_list.append(t_list)

        for i in range(1,num_entries(queasy.char1, ";")  + 1) :
            str = entry(i - 1, queasy.char1, ";")

            if substring(str, 0, 10) == ("$progname$").lower() :
                t_list.progavail = substring(str, 10)

            elif substring(str, 0, 9) == ("$htlcode$").lower() :
                t_list.hotelcode = substring(str, 9)

            elif substring(str, 0, 10) == ("$pushrate$").lower() :
                t_list.pushrate_flag = logical(substring(str, 10))

            elif substring(str, 0, 11) == ("$pushavail$").lower() :
                t_list.pushavail_flag = logical(substring(str, 11))

            elif substring(str, 0, 8) == ("$period$").lower() :
                t_list.period = to_int(substring(str, 8))

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 161) & (Queasy.number1 == becode)).order_by(Queasy._recid).all():
        t_push_list = T_push_list()
        t_push_list_list.append(t_push_list)

        t_push_list.rcodevhp = entry(0, queasy.char1, ";")
        t_push_list.rcodebe = entry(1, queasy.char1, ";")
        t_push_list.rmtypevhp = entry(2, queasy.char1, ";")
        t_push_list.rmytpebe = entry(3, queasy.char1, ";")
        t_push_list.argtvhp = entry(4, queasy.char1, ";")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    date_110 = htparam.fdate

    return generate_output()