from functions.additional_functions import *
import decimal
from models import Queasy

def pos_dashboard_checksessionbl(sessionid:str):
    session_ok = False
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal session_ok, queasy


        return {"session_ok": session_ok}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 230) &  (Queasy.char1 == sessionid)).first()

    if queasy:
        session_ok = False
    else:
        session_ok = True

    return generate_output()