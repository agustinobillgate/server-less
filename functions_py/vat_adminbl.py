#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def vat_adminbl(paramno:int, bezeich:string, fdecimal:Decimal, fchar:string):

    prepare_cache ([Htparam])

    success_flag = False
    htparam = None

    db_session = local_storage.db_session
    bezeich = bezeich.strip()
    fchar = fchar.strip()

    def generate_output():
        nonlocal success_flag, htparam
        nonlocal paramno, bezeich, fdecimal, fchar

        return {"success_flag": success_flag}


    # htparam = get_cache (Htparam, {"paramnr": [(eq, paramno)]})
    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == paramno)).with_for_update().first()

    if htparam:
        htparam.bezeichnung = bezeich
        htparam.fdecimal =  to_decimal(fdecimal)
        htparam.fchar = fchar


        success_flag = True
        pass

    return generate_output()