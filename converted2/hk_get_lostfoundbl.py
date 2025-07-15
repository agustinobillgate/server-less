#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.hk_lostfound_1bl import hk_lostfound_1bl

def hk_get_lostfoundbl(comments:string, sorttype:int, fr_date:date, to_date:date):
    s_list_data = []

    s_list = None

    s_list_data, S_list = create_model("S_list", {"nr":int, "betriebsnr":int, "s_recid":int, "date1":date, "zeit":string, "zinr":string, "userinit":string, "bezeich":string, "foundby":string, "submitted":string, "reportby":string, "report_date":date, "location":string, "refno":string, "phoneno":string, "claimby":string, "claim_date":date, "expired":date, "bemerk":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_data
        nonlocal comments, sorttype, fr_date, to_date


        nonlocal s_list
        nonlocal s_list_data

        return {"s-list": s_list_data}

    if comments == None:
        comments = ""
    s_list_data = get_output(hk_lostfound_1bl(1, comments, sorttype, fr_date, to_date, "", None))

    return generate_output()