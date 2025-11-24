#using conversion tools version: 1.0.0.117

# =======================
# Rulita, 31-10-2025
# Recompile prgram 
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
# =======================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Counters, Queasy, Res_history
from functions.next_counter_for_update import next_counter_for_update

def hk_lostfound_addbl(zinr:string, from_date:date, zeit:string, dept:int, 
                       reason:string, reportby:string, claim_date:date, phoneno:string, 
                       refno:string, foundby:string, location:string, submitted:string, user_init:string):

    prepare_cache ([Bediener, Counters, Queasy, Res_history])

    s_list_data = []
    num:int = 0
    claim_date_str:string = ""
    bediener = counters = queasy = res_history = None

    s_list = None

    s_list_data, S_list = create_model("S_list", {"nr":int, "betriebsnr":int, "s_recid":int, "date1":date, "zeit":string, "zinr":string, "userinit":string, "bezeich":string, "foundby":string, "submitted":string, "reportby":string, "claim_date":date, "location":string, "refno":string, "phoneno":string})

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    zinr = zinr.strip()
    zeit = zeit.strip()
    reason = reason.strip()
    reportby = reportby.strip()
    phoneno = phoneno.strip()
    refno = refno.strip()
    foundby = foundby.strip()
    location = location.strip()
    submitted = submitted.strip()


    def generate_output():
        nonlocal s_list_data, num, claim_date_str, bediener, counters, queasy, res_history
        nonlocal zinr, from_date, zeit, dept, reason, reportby, claim_date, phoneno, refno, foundby, location, submitted, user_init


        nonlocal s_list
        nonlocal s_list_data

        return {"s-list": s_list_data}

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:
        num = to_int(substring(zeit, 0, 2)) * 3600 +\
                to_int(substring(zeit, 2, 2)) * 60 + to_int(substring(zeit, 4, 2))

        # counters = get_cache (Counters, {"counter_no": [(eq, 11)]})

        # if not counters:
        #     counters = Counters()
        #     db_session.add(counters)

        #     counters.counter_no = 11
        #     counters.counter_bez = "Lost+Found Counter"


        # counters.counter = counters.counter + 1
        last_count, error_lock = get_output(next_counter_for_update(11))
        pass

        if claim_date == None:
            claim_date_str = ""
        else:
            claim_date_str = to_string(claim_date)
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 7
        queasy.date1 = from_date
        queasy.number1 = num
        queasy.char1 = zinr
        queasy.number2 = bediener.nr
        queasy.char2 = reason
        queasy.betriebsnr = dept
        # queasy.number3 = counters.counter
        queasy.number3 = last_count
        
        foundby = replace_str(foundby, "|", "")
        submitted = replace_str(submitted, "|", "")
        reportby = replace_str(reportby, "|", "")
        phoneno = replace_str(phoneno, "|", "")
        refno = replace_str(refno, "|", "")
        location = replace_str(location, "|", "")
        queasy.char3 = foundby +\
                "|" + submitted +\
                "|" + entry(0, reportby, chr_unicode(2)) +\
                "|" + to_string(claim_date_str) +\
                "|" + phoneno +\
                "|" + refno +\
                "|" + location

        if num_entries(reportby, chr_unicode(2)) > 1:
            queasy.char3 = queasy.char3 + "|" + "|" + "|" + entry(1, reportby, chr_unicode(2))
        pass
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.nr = queasy.number3
        s_list.date1 = queasy.date1
        s_list.zeit = to_string(queasy.number1, "HH:MM:SS")
        s_list.zinr = queasy.char1
        s_list.userinit = bediener.userinit
        s_list.bezeich = queasy.char2
        s_list.betriebsnr = queasy.betriebsnr
        s_list.foundby = foundby
        s_list.submitted = submitted
        s_list.reportby = reportby
        s_list.claim_date = claim_date
        s_list.s_recid = queasy._recid
        s_list.phoneno = phoneno
        s_list.refno = refno
        s_list.location = location


        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Add LostFound No" +\
                to_string(queasy.number3, ">>>9") +\
                " Room " + queasy.char1
        res_history.action = "HouseKeeping"

        pass
        pass

    return generate_output()