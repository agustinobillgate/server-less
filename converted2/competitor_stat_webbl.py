#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Akt_code, Zinrstat

def competitor_stat_webbl(from_date:date, to_date:date):

    prepare_cache ([Akt_code, Zinrstat])

    b1_list_data = []
    akt_code = zinrstat = None

    b1_list = None

    b1_list_data, B1_list = create_model("B1_list", {"datum":date, "betriebsnr":int, "bezeich":string, "zimmeranz":int, "personen":int, "logisumsatz":Decimal, "argtumsatz":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_data, akt_code, zinrstat
        nonlocal from_date, to_date


        nonlocal b1_list
        nonlocal b1_list_data

        return {"b1-list": b1_list_data}

    zinrstat_obj_list = {}
    zinrstat = Zinrstat()
    akt_code = Akt_code()
    for zinrstat.datum, zinrstat.betriebsnr, zinrstat.zimmeranz, zinrstat.personen, zinrstat.logisumsatz, zinrstat.argtumsatz, zinrstat._recid, akt_code.bezeich, akt_code._recid in db_session.query(Zinrstat.datum, Zinrstat.betriebsnr, Zinrstat.zimmeranz, Zinrstat.personen, Zinrstat.logisumsatz, Zinrstat.argtumsatz, Zinrstat._recid, Akt_code.bezeich, Akt_code._recid).join(Akt_code,(Akt_code.aktionscode == Zinrstat.betriebsnr) & (Akt_code.aktiongrup == 4)).filter(
             (Zinrstat.zinr == ("Competitor").lower()) & (Zinrstat.datum >= from_date) & (Zinrstat.datum <= to_date)).order_by(Zinrstat._recid).all():
        if zinrstat_obj_list.get(zinrstat._recid):
            continue
        else:
            zinrstat_obj_list[zinrstat._recid] = True


        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.datum = zinrstat.datum
        b1_list.betriebsnr = zinrstat.betriebsnr
        b1_list.bezeich = akt_code.bezeich
        b1_list.zimmeranz = zinrstat.zimmeranz
        b1_list.personen = zinrstat.personen
        b1_list.logisumsatz =  to_decimal(zinrstat.logisumsatz)
        b1_list.argtumsatz = to_int(zinrstat.argtumsatz)

    return generate_output()