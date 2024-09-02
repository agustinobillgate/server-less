from functions.additional_functions import *
import decimal
from models import Res_history, Bediener

def benutzer_zugriffbl(ch:str, nr:int, username:str, permissions:str, rec_id:int):
    res_history = bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_history, bediener


        return {}

    res_history = Res_history()
    db_session.add(res_history)

    res_history.nr = nr
    res_history.datum = get_current_date()
    res_history.zeit = get_current_time_in_seconds()
    res_history.action = "User Access"
    res_history.aenderung = "CHG Access Right of: " + username + " " +\
            permissions + "->" + ch

    res_history = db_session.query(Res_history).first()


    bediener = db_session.query(Bediener).filter(
            (Bediener._recid == rec_id)).first()
    bediener.permissions = ch

    bediener = db_session.query(Bediener).first()

    return generate_output()