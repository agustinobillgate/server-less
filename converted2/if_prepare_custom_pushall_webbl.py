#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam

def if_prepare_custom_pushall_webbl(becode:int):

    prepare_cache ([Queasy, Htparam])

    from_date = None
    to_date = None
    maxdate = None
    t_list_data = []
    t_push_list_data = []
    rmtype_list_data = []
    i:int = 0
    str:string = ""
    queasy = htparam = None

    t_list = t_push_list = rmtype_list = None

    t_list_data, T_list = create_model("T_list", {"progavail":string, "hotelcode":string, "pushrate_flag":bool, "pushavail_flag":bool, "period":int})
    t_push_list_data, T_push_list = create_model("T_push_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int, "license":int})
    rmtype_list_data, Rmtype_list = create_model("Rmtype_list", {"bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, maxdate, t_list_data, t_push_list_data, rmtype_list_data, i, str, queasy, htparam
        nonlocal becode


        nonlocal t_list, t_push_list, rmtype_list
        nonlocal t_list_data, t_push_list_data, rmtype_list_data

        return {"from_date": from_date, "to_date": to_date, "maxdate": maxdate, "t-list": t_list_data, "t-push-list": t_push_list_data, "rmtype-list": rmtype_list_data}

    queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, becode)]})

    if queasy:
        t_list = T_list()
        t_list_data.append(t_list)

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
        t_push_list_data.append(t_push_list)

        t_push_list.rcodevhp = entry(0, queasy.char1, ";")
        t_push_list.rcodebe = entry(1, queasy.char1, ";")
        t_push_list.rmtypevhp = entry(2, queasy.char1, ";")
        t_push_list.rmtypebe = entry(3, queasy.char1, ";")
        t_push_list.argtvhp = entry(4, queasy.char1, ";")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    from_date = htparam.fdate

    t_push_list = query(t_push_list_data, first=True)

    if t_push_list:
        rmtype_list = Rmtype_list()
        rmtype_list_data.append(rmtype_list)

        rmtype_list.bezeich = "*"

        for t_push_list in query(t_push_list_data):

            rmtype_list = query(rmtype_list_data, filters=(lambda rmtype_list: rmtype_list.bezeich == t_push_list.rmtypevhp), first=True)

            if not rmtype_list:
                rmtype_list = Rmtype_list()
                rmtype_list_data.append(rmtype_list)

                rmtype_list.bezeich = t_push_list.rmtypevhp

    t_list = query(t_list_data, first=True)

    if t_list:

        if t_list.period < 90:
            t_list.period = 90
        to_date = from_date + timedelta(days=t_list.period)
        maxdate = to_date

    return generate_output()