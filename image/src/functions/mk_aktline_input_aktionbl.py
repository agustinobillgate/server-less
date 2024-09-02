from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Akt_code

def mk_aktline_input_aktionbl(t_aktion:str):
    t_aktionscode = 0
    akt_code = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_aktionscode, akt_code


        return {"t_aktionscode": t_aktionscode}


    akt_code = db_session.query(Akt_code).filter(
            (Akt_code.aktiongrup == 1) &  (func.lower(Akt_code.bezeich) == (t_aktion).lower())).first()
    t_aktionscode = akt_code.aktionscode

    return generate_output()