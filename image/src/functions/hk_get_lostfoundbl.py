from functions.additional_functions import *
import decimal
from datetime import date
from functions.hk_lostfound_1bl import hk_lostfound_1bl

def hk_get_lostfoundbl(comments:str, sorttype:int, fr_date:date, to_date:date):
    s_list_list = []

    s_list = None

    s_list_list, S_list = create_model("S_list", {"nr":int, "betriebsnr":int, "s_recid":int, "date1":date, "zeit":str, "zinr":str, "userinit":str, "bezeich":str, "foundby":str, "submitted":str, "reportby":str, "report_date":date, "location":str, "refno":str, "phoneno":str, "claimby":str, "claim_date":date, "expired":date, "bemerk":str})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list
        nonlocal comments, sorttype, fr_date, to_date


        nonlocal s_list
        nonlocal s_list_list
        return {"s-list": s_list_list}

    if comments == None:
        comments = ""
    s_list_list = get_output(hk_lostfound_1bl(1, comments, sorttype, fr_date, to_date, "", None))

    return generate_output()