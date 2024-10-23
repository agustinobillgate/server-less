from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener, Akthdr, Akt_line, Guest, Res_history

def akthdr_list_btn_delbl(akthdr_recid:int, user_init:str):
    bediener = akthdr = akt_line = guest = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bediener, akthdr, akt_line, guest, res_history
        nonlocal akthdr_recid, user_init


        return {}


    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()

    akthdr = db_session.query(Akthdr).filter(
             (Akthdr._recid == akthdr_recid)).first()
    akthdr.flag = 0

    for akt_line in db_session.query(Akt_line).filter(
             (Akt_line.aktnr == akthdr.aktnr)).order_by(Akt_line._recid).all():
        akt_line.flag = 2

    guest = db_session.query(Guest).filter(
             (Guest.gastnr == akthdr.gastnr)).first()
    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = bediener.nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.aenderung = "Delete Activity: ActNo " + to_string(akthdr.aktnr) +\
            " - " + guest.name
    res_history.action = "Sales Activity"


    pass

    return generate_output()