#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zinrstat

slist_list, Slist = create_model("Slist", {"datum":date, "hnr":int, "hname":string, "totrm":int, "occrm":int, "comrm":int, "rmrev":Decimal})

def competitor_adm_update_it_1bl(from_date:date, to_date:date, slist_list:[Slist]):
    zinrstat = None

    slist = tlist = buf_zinrstat = None

    tlist_list, Tlist = create_model("Tlist", {"datum":date})

    Buf_zinrstat = create_buffer("Buf_zinrstat",Zinrstat)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal zinrstat
        nonlocal from_date, to_date
        nonlocal buf_zinrstat


        nonlocal slist, tlist, buf_zinrstat
        nonlocal tlist_list

        return {}


    for zinrstat in db_session.query(Zinrstat).filter(
             (Zinrstat.zinr == ("Competitor").lower()) & (Zinrstat.datum >= from_date) & (Zinrstat.datum <= to_date)).order_by(Zinrstat._recid).all():
        db_session.delete(zinrstat)

    for slist in query(slist_list):
        zinrstat = Zinrstat()
        db_session.add(zinrstat)

        zinrstat.zinr = "Competitor"
        zinrstat.datum = slist.datum
        zinrstat.betriebsnr = slist.hnr
        zinrstat.zimmeranz = slist.totrm
        zinrstat.personen = slist.occrm
        zinrstat.argtumsatz =  to_decimal(to_decimal(slist.comrm) )
        zinrstat.logisumsatz =  to_decimal(slist.rmrev)


        pass

    return generate_output()