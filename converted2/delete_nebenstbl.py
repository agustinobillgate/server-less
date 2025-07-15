#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Nebenst

def delete_nebenstbl(case_type:int, int1:int):
    successflag = False
    nebenst = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, nebenst
        nonlocal case_type, int1

        return {"successflag": successflag}


    if case_type == 1:

        nebenst = get_cache (Nebenst, {"_recid": [(eq, int1)]})

        if nebenst:
            db_session.delete(nebenst)
            pass
            successflag = True

    return generate_output()