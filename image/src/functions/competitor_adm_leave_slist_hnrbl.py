from functions.additional_functions import *
import decimal
from models import Akt_code

def competitor_adm_leave_slist_hnrbl(slist_hnr:int):
    avail_akt_code = False
    akt_code_bezeich = ""
    akt_code = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_akt_code, akt_code_bezeich, akt_code


        return {"avail_akt_code": avail_akt_code, "akt_code_bezeich": akt_code_bezeich}


    akt_code = db_session.query(Akt_code).filter(
            (Akt_code.aktiongrup == 4) &  (Akt_code.aktionscode == slist_hnr)).first()

    if akt_code:
        avail_akt_code = True
        akt_code_bezeich = akt_code.bezeich

    return generate_output()