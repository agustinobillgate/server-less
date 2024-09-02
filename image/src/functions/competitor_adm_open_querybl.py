from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zinrstat, Akt_code

def competitor_adm_open_querybl(from_date:date, to_date:date):
    slist_list = []
    zinrstat = akt_code = None

    slist = None

    slist_list, Slist = create_model("Slist", {"datum":date, "hnr":int, "hname":str, "totrm":int, "occrm":int, "comrm":int, "rmrev":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal slist_list, zinrstat, akt_code


        nonlocal slist
        nonlocal slist_list
        return {"slist": slist_list}


    slist_list.clear()

    for zinrstat in db_session.query(Zinrstat).filter(
            (func.lower(Zinrstat.zinr) == "Competitor") &  (Zinrstat.datum >= from_date) &  (Zinrstat.datum <= to_date)).all():
        slist = Slist()
        slist_list.append(slist)

        slist.datum = zinrstat.datum
        slist.hnr = zinrstat.betriebsnr
        slist.totrm = zinrstat.zimmeranz
        slist.occrm = zinrstat.personen
        slist.comrm = to_int(zinrstat.argtumsatz)
        slist.rmrev = zinrstat.logisumsatz

        akt_code = db_session.query(Akt_code).filter(
                (Akt_code.aktionscode == zinrstat.betriebsnr) &  (Akt_code.aktiongrup == 4)).first()

        if akt_code:
            slist.hname = akt_code.bezeich

    return generate_output()