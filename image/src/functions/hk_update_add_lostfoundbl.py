from functions.additional_functions import *
import decimal
from datetime import date
from functions.hk_lostfound_chgbl import hk_lostfound_chgbl
from functions.hk_lostfound_addbl import hk_lostfound_addbl

def hk_update_add_lostfoundbl(rec_id:int, zinr:str, item_description:str, from_date:date, zeit:str, dept:int, remark:str, claimby:str, claim_date:date, expired_date:date, reportedby:str, report_date:date, phoneno:str, refno:str, foundby:str, location:str, submitted:str, user_init:str):
    s_list_list = []
    expired_str:str = ""
    claim_date_str:str = ""

    s_list = None

    s_list_list, S_list = create_model("S_list", {"nr":int, "betriebsnr":int, "s_recid":int, "date1":date, "zeit":str, "zinr":str, "userinit":str, "bezeich":str, "foundby":str, "submitted":str, "claimby":str, "claim_date":date, "location":str, "refno":str, "phoneno":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, expired_str, claim_date_str
        nonlocal rec_id, zinr, item_description, from_date, zeit, dept, remark, claimby, claim_date, expired_date, reportedby, report_date, phoneno, refno, foundby, location, submitted, user_init


        nonlocal s_list
        nonlocal s_list_list
        return {"s-list": s_list_list}

    if rec_id != None and rec_id != 0:
        s_list = S_list()
        s_list_list.append(s_list)

        s_list.s_recid = rec_id

    if zinr == None:
        zinr = ""

    if from_date == None:
        from_date = get_current_date()

    if zeit == None:
        zeit = substring(to_string(time, "HH:MM:SS") , 0, 2) + substring(to_string(time, "HH:MM:SS") , 3, 2) + substring(to_string(time, "HH:MM:SS") , 6, 2)

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
        s_list_list = get_output(hk_lostfound_chgbl(zinr, from_date, zeit, dept, item_description + chr(2) + remark, reportedby + chr(2) + claimby + chr(2) + claim_date_str + chr(2) + expired_str, report_date, phoneno, refno, foundby, location, submitted, user_init, s_list_list))
    else:
        s_list_list = get_output(hk_lostfound_addbl(zinr, from_date, zeit, dept, item_description + chr(2) + remark, reportedby + chr(2) + expired_str, report_date, phoneno, refno, foundby, location, submitted, user_init))

    return generate_output()