#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.hk_lostfound_chgbl import hk_lostfound_chgbl
from functions.hk_lostfound_addbl import hk_lostfound_addbl

def hk_update_add_lostfoundbl(rec_id:int, zinr:string, item_description:string, from_date:date, zeit:string, dept:int, remark:string, claimby:string, claim_date:date, expired_date:date, reportedby:string, report_date:date, phoneno:string, refno:string, foundby:string, location:string, submitted:string, user_init:string):
    s_list_data = []
    expired_str:string = ""
    claim_date_str:string = ""

    s_list = None

    s_list_data, S_list = create_model("S_list", {"nr":int, "betriebsnr":int, "s_recid":int, "date1":date, "zeit":string, "zinr":string, "userinit":string, "bezeich":string, "foundby":string, "submitted":string, "claimby":string, "claim_date":date, "location":string, "refno":string, "phoneno":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_data, expired_str, claim_date_str
        nonlocal rec_id, zinr, item_description, from_date, zeit, dept, remark, claimby, claim_date, expired_date, reportedby, report_date, phoneno, refno, foundby, location, submitted, user_init


        nonlocal s_list
        nonlocal s_list_data

        return {"s-list": s_list_data}

    if rec_id != None and rec_id != 0:
        s_list = S_list()
        s_list_data.append(s_list)

        s_list.s_recid = rec_id

    if zinr == None:
        zinr = ""

    if from_date == None:
        from_date = get_current_date()

    if zeit == None:
        zeit = substring(to_string(get_current_time_in_seconds(), "HH:MM:SS") , 0, 2) + substring(to_string(get_current_time_in_seconds(), "HH:MM:SS") , 3, 2) + substring(to_string(get_current_time_in_seconds(), "HH:MM:SS") , 6, 2)

    if remark == None:
        remark = ""

    if claimby == None:
        claimby = ""

    if phoneno == None:
        phoneno = ""

    if reportedby == None:
        reportedby = ""

    if refno == None:
        refno = ""

    if foundby == None:
        foundby = ""

    if location == None:
        location = ""

    if submitted == None:
        submitted = ""

    if item_description == None:
        item_description = ""

    if expired_date == None:
        expired_str = "99/99/99"
    else:
        expired_str = to_string(expired_date)

    if claim_date == None:
        claim_date_str = "99/99/99"
    else:
        claim_date_str = to_string(claim_date)

    if s_list:
        s_list_data = get_output(hk_lostfound_chgbl(zinr, from_date, zeit, dept, item_description + chr_unicode(2) + remark, reportedby + chr_unicode(2) + claimby + chr_unicode(2) + claim_date_str + chr_unicode(2) + expired_str, report_date, phoneno, refno, foundby, location, submitted, user_init, s_list_data))
    else:
        s_list_data = get_output(hk_lostfound_addbl(zinr, from_date, zeit, dept, item_description + chr_unicode(2) + remark, reportedby + chr_unicode(2) + expired_str, report_date, phoneno, refno, foundby, location, submitted, user_init))

    return generate_output()