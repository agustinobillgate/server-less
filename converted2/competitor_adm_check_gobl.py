#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zinrstat

slist_data, Slist = create_model("Slist", {"datum":date, "hnr":int, "hname":string, "totrm":int, "occrm":int, "comrm":int, "rmrev":Decimal})

def competitor_adm_check_gobl(slist_data:[Slist], pvilanguage:int, curr_mode:string):
    msg_str = ""
    lvcarea:string = "competitor-adm"
    zinrstat = None

    slist = sbuff = None

    Sbuff = Slist
    sbuff_data = slist_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, zinrstat
        nonlocal pvilanguage, curr_mode
        nonlocal sbuff


        nonlocal slist, sbuff

        return {"msg_str": msg_str}

    if curr_mode.lower()  == ("new").lower() :

        for slist in query(slist_data):

            zinrstat = get_cache (Zinrstat, {"datum": [(eq, slist.datum)],"zinr": [(eq, "competitor")],"betriebsnr": [(eq, slist.hnr)]})

            if zinrstat:
                msg_str = "&W" + translateExtended ("Statistic record found for date", lvcarea, "") + " " + to_string(slist.datum) + " " + translateExtended ("hotel number", lvcarea, "") + to_string(slist.hnr) + "!"

                return generate_output()

    for sbuff in query(sbuff_data):

        slist = query(slist_data, filters=(lambda slist: slist.datum == sbuff.datum and slist.hnr == sbuff.hnr and slist._recid != sbuff._recid), first=True)

        if slist:
            msg_str = "&W" + translateExtended ("Duplicate Records found for date ", lvcarea, "") + " " + to_string(slist.datum) + " " + translateExtended ("Hotel", lvcarea, "") + " " + to_string(slist.hnr) + "!"

            return generate_output()

    return generate_output()