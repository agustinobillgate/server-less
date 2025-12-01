#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Akthdr, Akt_line, Guest, Res_history

def akt_sales1_btn_delbl(recid_akthdr:int, bediener_nr:int):

    prepare_cache ([Akthdr, Akt_line, Res_history])

    akthdr = akt_line = guest = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal akthdr, akt_line, guest, res_history
        nonlocal recid_akthdr, bediener_nr

        return {}


    # akthdr = get_cache (Akthdr, {"_recid": [(eq, recid_akthdr)]})
    akthdr = db_session.query(Akthdr).filter(Akthdr._recid == recid_akthdr).with_for_update().first()
    akthdr.flag = 0

    for akt_line in db_session.query(Akt_line).filter(
             (Akt_line.aktnr == akthdr.aktnr)).order_by(Akt_line._recid).with_for_update().all():
        akt_line.flag = 2


    guest = get_cache (Guest, {"gastnr": [(eq, akthdr.gastnr)]})
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener_nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "Delete Activity: ActNo " + to_string(akthdr.aktnr) +\
            " - " + guest.name
    res_history.action = "Sales Activity"


    return generate_output()