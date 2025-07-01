#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zinrstat, Akt_code

def competitor_adm_copy_itbl():

    prepare_cache ([Zinrstat, Akt_code])

    slist_list = []
    curr_date:date = None
    zinrstat = akt_code = None

    slist = None

    slist_list, Slist = create_model("Slist", {"datum":date, "hnr":int, "hname":string, "totrm":int, "occrm":int, "comrm":int, "rmrev":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal slist_list, curr_date, zinrstat, akt_code


        nonlocal slist
        nonlocal slist_list

        return {"slist": slist_list}


    slist_list.clear()

    for zinrstat in db_session.query(Zinrstat).filter(
             (Zinrstat.zinr == ("Competitor").lower())).order_by(Zinrstat.datum.desc()).all():

        if curr_date != None and curr_date != zinrstat.datum:
            break
        slist = Slist()
        slist_list.append(slist)

        slist.datum = zinrstat.datum + timedelta(days=1)
        slist.hnr = zinrstat.betriebsnr
        slist.totrm = zinrstat.zimmeranz
        curr_date = zinrstat.datum

        akt_code = get_cache (Akt_code, {"aktionscode": [(eq, zinrstat.betriebsnr)],"aktiongrup": [(eq, 4)]})

        if akt_code:
            slist.hname = akt_code.bezeich

    return generate_output()