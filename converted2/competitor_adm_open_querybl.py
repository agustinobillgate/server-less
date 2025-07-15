#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zinrstat, Akt_code

def competitor_adm_open_querybl(from_date:date, to_date:date):

    prepare_cache ([Zinrstat, Akt_code])

    slist_data = []
    zinrstat = akt_code = None

    slist = None

    slist_data, Slist = create_model("Slist", {"datum":date, "hnr":int, "hname":string, "totrm":int, "occrm":int, "comrm":int, "rmrev":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal slist_data, zinrstat, akt_code
        nonlocal from_date, to_date


        nonlocal slist
        nonlocal slist_data

        return {"slist": slist_data}


    slist_data.clear()

    for zinrstat in db_session.query(Zinrstat).filter(
             (Zinrstat.zinr == ("Competitor").lower()) & (Zinrstat.datum >= from_date) & (Zinrstat.datum <= to_date)).order_by(Zinrstat._recid).all():
        slist = Slist()
        slist_data.append(slist)

        slist.datum = zinrstat.datum
        slist.hnr = zinrstat.betriebsnr
        slist.totrm = zinrstat.zimmeranz
        slist.occrm = zinrstat.personen
        slist.comrm = to_int(zinrstat.argtumsatz)
        slist.rmrev =  to_decimal(zinrstat.logisumsatz)

        akt_code = get_cache (Akt_code, {"aktionscode": [(eq, zinrstat.betriebsnr)],"aktiongrup": [(eq, 4)]})

        if akt_code:
            slist.hname = akt_code.bezeich

    return generate_output()