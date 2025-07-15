#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Fixleist

def delete_fixleistbl(case_type:int, int1:int):
    succesflag = False
    fixleist = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal succesflag, fixleist
        nonlocal case_type, int1

        return {"succesflag": succesflag}


    if case_type == 1:

        fixleist = get_cache (Fixleist, {"_recid": [(eq, int1)]})

        if fixleist:
            db_session.delete(fixleist)
            pass
            succesflag = True

    return generate_output()