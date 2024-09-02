from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zinrstat

def competitor_adm_update_itbl(slist:[Slist]):
    zinrstat = None

    slist = None

    slist_list, Slist = create_model("Slist", {"datum":date, "hnr":int, "hname":str, "totrm":int, "occrm":int, "comrm":int, "rmrev":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal zinrstat


        nonlocal slist
        nonlocal slist_list
        return {}

    for slist in query(slist_list):

        zinrstat = db_session.query(Zinrstat).filter(
                (func.lower(Zinrstat.zinr) == "Competitor") &  (Zinrstat.datum == slist.datum) &  (Zinrstat.betriebsnr == slist.hnr)).first()

        if zinrstat:
            zinrstat.zimmeranz = slist.totrm
            zinrstat.personen = slist.occrm
            zinrstat.argtumsatz = decimal.Decimal(slist.comrm)
            zinrstat.logisumsatz = slist.rmrev

            zinrstat = db_session.query(Zinrstat).first()

    return generate_output()