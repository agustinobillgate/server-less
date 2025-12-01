#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 28-11-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zinrstat

slist_data, Slist = create_model("Slist", {"datum":date, "hnr":int, "hname":string, "totrm":int, "occrm":int, "comrm":int, "rmrev":Decimal})

def competitor_adm_update_itbl(slist_data:[Slist]):

    prepare_cache ([Zinrstat])

    zinrstat = None

    slist = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal zinrstat


        nonlocal slist

        return {}

    for slist in query(slist_data):

        # zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "competitor")],"datum": [(eq, slist.datum)],"betriebsnr": [(eq, slist.hnr)]})
        zinrstat = db_session.query(Zinrstat).filter(
                 (Zinrstat.zinr == "competitor") & (Zinrstat.datum == slist.datum) & (Zinrstat.betriebsnr == slist.hnr)).with_for_update().first()

        if zinrstat:
            zinrstat.zimmeranz = slist.totrm
            zinrstat.personen = slist.occrm
            zinrstat.argtumsatz =  to_decimal(to_decimal(slist.comrm) )
            zinrstat.logisumsatz =  to_decimal(slist.rmrev)
            # pass

    return generate_output()
