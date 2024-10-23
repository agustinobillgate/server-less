from functions.additional_functions import *
import decimal
from models import Akthdr, Akt_line, Guest, Res_history

def akt_sales1_btn_delbl(recid_akthdr:int, bediener_nr:int):
    akthdr = akt_line = guest = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal akthdr, akt_line, guest, res_history
        nonlocal recid_akthdr, bediener_nr


        return {}


    akthdr = db_session.query(Akthdr).filter(
             (Akthdr._recid == recid_akthdr)).first()
    akthdr.flag = 0

    for akt_line in db_session.query(Akt_line).filter(
             (Akt_line.aktnr == akthdr.aktnr)).order_by(Akt_line._recid).all():
        akt_line.flag = 2

    guest = db_session.query(Guest).filter(
             (Guest.gastnr == akthdr.gastnr)).first()
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener_nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "Delete Activity: ActNo " + to_string(akthdr.aktnr) +\
            " - " + guest.name
    res_history.action = "Sales Activity"


    pass

    return generate_output()