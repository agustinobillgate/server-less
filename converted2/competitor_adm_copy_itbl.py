#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zinrstat, Akt_code

def competitor_adm_copy_itbl():

    prepare_cache ([Zinrstat, Akt_code])

    slist_data = []
    curr_date:date = None
    zinrstat = akt_code = None

    slist = None

    slist_data, Slist = create_model("Slist", {"datum":date, "hnr":int, "hname":string, "totrm":int, "occrm":int, "comrm":int, "rmrev":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal slist_data, curr_date, zinrstat, akt_code


        nonlocal slist
        nonlocal slist_data

        return {"slist": slist_data}


    slist_data.clear()

    for zinrstat in db_session.query(Zinrstat).filter(
             (Zinrstat.zinr == ("Competitor").lower())).order_by(Zinrstat.datum.desc()).all():

        if curr_date != None and curr_date != zinrstat.datum:
            break
        slist = Slist()
        slist_data.append(slist)

        slist.datum = zinrstat.datum + timedelta(days=1)
        slist.hnr = zinrstat.betriebsnr
        slist.totrm = zinrstat.zimmeranz
        curr_date = zinrstat.datum

        akt_code = get_cache (Akt_code, {"aktionscode": [(eq, zinrstat.betriebsnr)],"aktiongrup": [(eq, 4)]})

        if akt_code:
            slist.hname = akt_code.bezeich

    return generate_output()