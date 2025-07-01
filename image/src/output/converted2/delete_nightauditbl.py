#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Nightaudit

def delete_nightauditbl(case_type:int, int1:int):
    successflag = False
    nightaudit = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, nightaudit
        nonlocal case_type, int1

        return {"successflag": successflag}


    if case_type == 1:

        nightaudit = get_cache (Nightaudit, {"_recid": [(eq, int1)]})

        if nightaudit:
            db_session.delete(nightaudit)
            pass
            successflag = True

    return generate_output()