#using conversion tools version: 1.0.0.117

# ===============================================================
# Rulita, 31-10-2025
# Recompile prgram 
# Masih menunggu PakM makesure var claimby & claim_date dari mana
# s_list.claimby = s_list.claimby
# s_list.claim_date = s_list.claim_date
# ===============================================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Bediener, Res_history

s_list_data, S_list = create_model("S_list", {"nr":int, "betriebsnr":int, "s_recid":int, "date1":date, "zeit":string, "zinr":string, "userinit":string, "bezeich":string, "foundby":string, "submitted":string, "claimby":string, "claim_date":date, "location":string, "refno":string, "phoneno":string})

def hk_lostfound_chgbl(zinr:string, from_date:date, zeit:string, dept:int, reason:string, reportedby:string, report_date:date, phoneno:string, refno:string, foundby:string, location:string, submitted:string, user_init:string, s_list_data:[S_list]):

    prepare_cache ([Queasy, Bediener, Res_history])

    num:int = 0
    report_date_str:string = ""
    t_str:string = ""
    queasy = bediener = res_history = None

    s_list = t_qsy = None

    T_qsy = create_buffer("T_qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal num, report_date_str, t_str, queasy, bediener, res_history
        nonlocal zinr, from_date, zeit, dept, reason, reportedby, report_date, phoneno, refno, foundby, location, submitted, user_init
        nonlocal t_qsy


        nonlocal s_list, t_qsy

        return {"s-list": s_list_data}

    s_list = query(s_list_data, first=True)

    if report_date == None:
        report_date_str = ""
    else:
        report_date_str = to_string(report_date)
    num = to_int(substring(zeit, 0, 2)) * 3600 +\
            to_int(substring(zeit, 2, 2)) * 60 + to_int(substring(zeit, 4, 2))

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:

        t_qsy = get_cache (Queasy, {"_recid": [(eq, s_list.s_recid)]})

        queasy = get_cache (Queasy, {"_recid": [(eq, s_list.s_recid)]})

        if t_qsy.betriebsnr != dept:

            if dept == 0:
                t_str = t_str + " Found->Lost"
            else:
                t_str = t_str + " Lost->Found"

        if t_qsy.char1.lower()  != (zinr).lower() :
            t_str = t_str + " Room " + t_qsy.char1 + "->" + zinr

        if t_qsy.date1 != from_date:
            t_str = t_str + " Date " + to_string(t_qsy.date1, "99/99/99") + "->" + to_string(from_date, "99/99/99")

        if t_qsy.number1 != num:
            t_str = t_str + " Time " + to_string(t_qsy.number1, "hh:mm:ss") + "->" + to_string(num, "HH:MM:SS")

        if entry(0, t_qsy.char2, chr_unicode(2)) != entry(0, reason, chr_unicode(2)):
            t_str = t_str + " Item " + entry(0, t_qsy.char2, chr_unicode(2)) + "->" + entry(0, reason, chr_unicode(2))

        if entry(1, t_qsy.char2, chr_unicode(2)) != entry(1, reason, chr_unicode(2)):
            t_str = t_str + " Remark " + entry(1, t_qsy.char2, chr_unicode(2)) + "->" + entry(1, reason, chr_unicode(2))

        if entry(0, t_qsy.char3, chr_unicode(124)) != (foundby).lower() :
            t_str = t_str + " foundby " + entry(0, t_qsy.char3, chr_unicode(124)) + "->" + foundby

        if entry(1, t_qsy.char3, chr_unicode(124)) != (submitted).lower() :
            t_str = t_str + " SubmittedTo " + entry(1, t_qsy.char3, chr_unicode(124)) + "->" + submitted

        if entry(2, t_qsy.char3, chr_unicode(124)) != entry(0, reportedby, chr_unicode(2)):
            t_str = t_str + " reportedby " + entry(2, t_qsy.char3, chr_unicode(124)) + "->" + entry(0, reportedby, chr_unicode(2))

        if entry(3, t_qsy.char3, chr_unicode(124)) != to_string(report_date, "99/99/99"):
            t_str = t_str + " ReportedDate " + entry(3, t_qsy.char3, chr_unicode(124)) + "->" + to_string(report_date, "99/99/99")

        if entry(4, t_qsy.char3, chr_unicode(124)) != phoneno:
            t_str = t_str + " ReportedPhone " + entry(4, t_qsy.char3, chr_unicode(124)) + "->" + phoneno

        if entry(5, t_qsy.char3, chr_unicode(124)) != refno:
            t_str = t_str + " RefNum " + entry(5, t_qsy.char3, chr_unicode(124)) + "->" + refno

        if entry(6, t_qsy.char3, chr_unicode(124)) != (location).lower() :
            t_str = t_str + " location " + entry(6, t_qsy.char3, chr_unicode(124)) + "->" + location

        if entry(7, t_qsy.char3, chr_unicode(124)) != entry(1, reportedby, chr_unicode(2)):
            t_str = t_str + " ClaimedBy " + entry(7, t_qsy.char3, chr_unicode(124)) + "->" + entry(1, reportedby, chr_unicode(2))

        if entry(8, t_qsy.char3, chr_unicode(124)) != entry(2, reportedby, chr_unicode(2)):
            t_str = t_str + " ClaimedDate " + entry(8, t_qsy.char3, chr_unicode(124)) + "->" + entry(2, reportedby, chr_unicode(2))

        if entry(9, t_qsy.char3, chr_unicode(124)) != entry(3, reportedby, chr_unicode(2)):
            t_str = t_str + " ExpiredDate " + entry(9, t_qsy.char3, chr_unicode(124)) + "->" + entry(3, reportedby, chr_unicode(2))
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
                " Room " + queasy.char1 +\
                " : " + t_str


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
        s_list.claimby = s_list.claimby             # Rulita, Masi di makesure ke pakM
        s_list.claim_date = s_list.claim_date       # Rulita, Masi di makesure ke pakM
        s_list.s_recid = queasy._recid
        s_list.phoneno = phoneno
        s_list.refno = refno
        s_list.location = location

    return generate_output()