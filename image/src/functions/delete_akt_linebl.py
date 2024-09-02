from functions.additional_functions import *
import decimal
from models import Akt_line

def delete_akt_linebl(case_type:int, aktnr:int):
    success_flag = False
    akt_line = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, akt_line


        return {"success_flag": success_flag}


    if case_type == 1:

        for akt_line in db_session.query(Akt_line).filter(
                (Akt_line.aktnr == aktnr)).all():
            db_session.delete(akt_line)

            success_flag = True

    return generate_output()