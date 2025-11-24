#using conversion tools version: 1.0.0.117
#--------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#--------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Gl_acct

def delete_gl_acctbl(case_type:int, int1:int, char1:string):
    success_flag = False
    gl_acct = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, gl_acct
        nonlocal case_type, int1, char1

        return {"success_flag": success_flag}


    if case_type == 1:
        # Rd, 24/11/2025, get gl_acct dengan key, _recid
        # gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, char1)]})
        gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == char1)).with_for_update().first()

        if gl_acct:
            db_session.delete(gl_acct)
            pass
            success_flag = True

    return generate_output()