from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zinrstat

def competitor_adm_check_gobl(slist:[Slist], pvilanguage:int, curr_mode:str):
    msg_str = ""
    lvcarea:str = "competitor_adm"
    zinrstat = None

    slist = sbuff = None

    slist_list, Slist = create_model("Slist", {"datum":date, "hnr":int, "hname":str, "totrm":int, "occrm":int, "comrm":int, "rmrev":decimal})

    Sbuff = Slist
    sbuff_list = slist_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, zinrstat
        nonlocal sbuff


        nonlocal slist, sbuff
        nonlocal slist_list
        return {"msg_str": msg_str}

    if curr_mode.lower()  == "new":

        for slist in query(slist_list):

            zinrstat = db_session.query(Zinrstat).filter(
                    (Zinrstat.datum == slist.datum) &  (func.lower(Zinrstat.zinr) == "Competitor") &  (Zinrstat.betriebsnr == slist.hnr)).first()

            if zinrstat:
                msg_str = "&W" + translateExtended ("Statistic record found for date", lvcarea, "") + " " + to_string(slist.datum) + " " + translateExtended ("hotel number", lvcarea, "") + to_string(slist.hnr) + "!"

                return generate_output()

    for sbuff in query(sbuff_list):

        slist = query(slist_list, filters=(lambda slist :slist.datum == sbuff.datum and slist.hnr == sbuff.hnr and slist._recid != sbuff._recid), first=True)

        if slist:
            msg_str = "&W" + translateExtended ("Duplicate Records found for date ", lvcarea, "") + " " + to_string(slist.datum) + " " + translateExtended ("Hotel", lvcarea, "") + " " + to_string(slist.hnr) + "!"

            return generate_output()