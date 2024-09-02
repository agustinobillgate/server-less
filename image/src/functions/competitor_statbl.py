from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Akt_code, Zinrstat

def competitor_statbl(from_date:date, to_date:date):
    b1_list_list = []
    akt_code = zinrstat = None

    b1_list = None

    b1_list_list, B1_list = create_model("B1_list", {"datum":date, "betriebsnr":int, "bezeich":str, "zimmeranz":int, "personen":int, "logisumsatz":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, akt_code, zinrstat


        nonlocal b1_list
        nonlocal b1_list_list
        return {"b1-list": b1_list_list}

    zinrstat_obj_list = []
    for zinrstat, akt_code in db_session.query(Zinrstat, Akt_code).join(Akt_code,(Akt_code.aktionscode == Zinrstat.betriebsnr) &  (Akt_code.aktiongrup == 4)).filter(
            (func.lower(Zinrstat.zinr) == "Competitor") &  (Zinrstat.datum >= from_date) &  (Zinrstat.datum <= to_date)).all():
        if zinrstat._recid in zinrstat_obj_list:
            continue
        else:
            zinrstat_obj_list.append(zinrstat._recid)


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.datum = zinrstat.datum
        b1_list.betriebsnr = zinrstat.betriebsnr
        b1_list.bezeich = akt_code.bezeich
        b1_list.zimmeranz = zinrstat.zimmeranz
        b1_list.personen = zinrstat.personen
        b1_list.logisumsatz = zinrstat.logisumsatz

    return generate_output()