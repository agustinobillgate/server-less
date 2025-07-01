#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Queasy, Res_history

s_list_list, S_list = create_model("S_list", {"nr":int, "betriebsnr":int, "s_recid":int, "date1":date, "zeit":string, "zinr":string, "userinit":string, "bezeich":string, "foundby":string, "submitted":string, "claimby":string, "claim_date":date, "location":string, "refno":string, "phoneno":string})

def hk_lostfound_chgbl(zinr:string, from_date:date, zeit:string, dept:int, reason:string, reportedby:string, report_date:date, phoneno:string, refno:string, foundby:string, location:string, submitted:string, user_init:string, s_list_list:[S_list]):

    prepare_cache ([Bediener, Queasy, Res_history])

    num:int = 0
    report_date_str:string = ""
    bediener = queasy = res_history = None

    s_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal num, report_date_str, bediener, queasy, res_history
        nonlocal zinr, from_date, zeit, dept, reason, reportedby, report_date, phoneno, refno, foundby, location, submitted, user_init


        nonlocal s_list

        return {"s-list": s_list_list}

    s_list = query(s_list_list, first=True)

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if report_date == None:
        report_date_str = ""
    else:
        report_date_str = to_string(report_date)
    num = to_int(substring(zeit, 0, 2)) * 3600 +\
            to_int(substring(zeit, 2, 2)) * 60 + to_int(substring(zeit, 4, 2))

    queasy = get_cache (Queasy, {"_recid": [(eq, s_list.s_recid)]})
    queasy.key = 7
    queasy.date1 = from_date
    queasy.number1 = num
    queasy.char1 = zinr
    queasy.number2 = bediener.nr
    queasy.char2 = reason
    queasy.betriebsnr = dept
    foundby = replace_str(foundby, "|", "")
    submitted = replace_str(submitted, "|", "")
    reportedby = replace_str(reportedby, "|", "")
    phoneno = replace_str(phoneno, "|", "")
    refno = replace_str(refno, "|", "")
    location = replace_str(location, "|", "")
    queasy.char3 = foundby +\
            "|" + submitted +\
            "|" + entry(0, reportedby, chr_unicode(2)) +\
            "|" + to_string(report_date_str) +\
            "|" + phoneno +\
            "|" + refno +\
            "|" + location

    if num_entries(reportedby, chr_unicode(2)) > 1:
        queasy.char3 = queasy.char3 +\
            "|" + entry(1, reportedby, chr_unicode(2)) +\
            "|" + entry(2, reportedby, chr_unicode(2)) +\
            "|" + entry(3, reportedby, chr_unicode(2))


    pass
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "Change LostFound No " +\
            to_string(queasy.number3, ">>>,>>9") +\
            " Room " + queasy.char1
    res_history.action = "HouseKeeping"


    pass
    pass
    s_list.nr = queasy.number3
    s_list.date1 = queasy.date1
    s_list.zeit = to_string(queasy.number1, "HH:MM:SS")
    s_list.zinr = queasy.char1
    s_list.userinit = bediener.userinit
    s_list.bezeich = queasy.char2
    s_list.betriebsnr = queasy.betriebsnr
    s_list.foundby = foundby
    s_list.submitted = submitted
    s_list.claimby = claimBy
    s_list.claim_date = claim_date
    s_list.s_recid = queasy._recid
    s_list.phoneno = phoneno
    s_list.refno = refno
    s_list.location = location

    return generate_output()