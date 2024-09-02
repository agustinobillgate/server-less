from functions.additional_functions import *
import decimal
from datetime import date
from models import Zinrstat

def competitor_adm_add_itbl(slist:[Slist]):
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
        zinrstat = Zinrstat()
        db_session.add(zinrstat)

        zinrstat.zinr = "Competitor"
        zinrstat.datum = slist.datum
        zinrstat.betriebsnr = slist.hnr
        zinrstat.zimmeranz = slist.totrm
        zinrstat.personen = slist.occrm
        zinrstat.argtumsatz = decimal.Decimal(slist.comrm)
        zinrstat.logisumsatz = slist.rmrev

        zinrstat = db_session.query(Zinrstat).first()

    return generate_output()