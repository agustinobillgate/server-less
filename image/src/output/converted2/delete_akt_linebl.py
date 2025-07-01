#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Akt_line

def delete_akt_linebl(case_type:int, aktnr:int):
    success_flag = False
    akt_line = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, akt_line
        nonlocal case_type, aktnr

        return {"success_flag": success_flag}


    if case_type == 1:

        for akt_line in db_session.query(Akt_line).filter(
                 (Akt_line.aktnr == aktnr)).order_by(Akt_line._recid).all():
            db_session.delete(akt_line)
            pass
            success_flag = True

    return generate_output()