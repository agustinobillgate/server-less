from functions.additional_functions import *
import decimal
from models import Akt_code, Akt_line

def aktcode_admin_btn_delnamebl(akt_code_aktionscode:int, recid_akt_code:int):
    erase_flag = False
    akt_code = akt_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal erase_flag, akt_code, akt_line
        nonlocal akt_code_aktionscode, recid_akt_code


        return {"erase_flag": erase_flag}


    akt_code = db_session.query(Akt_code).filter(
             (Akt_code._recid == recid_akt_code)).first()

    akt_line = db_session.query(Akt_line).filter(
             (Akt_line.aktionscode == akt_code_aktionscode)).first()

    if akt_line:
        pass
    else:
        db_session.delete(akt_code)
        erase_flag = True

    return generate_output()