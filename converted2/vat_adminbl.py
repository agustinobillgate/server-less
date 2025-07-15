#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def vat_adminbl(paramno:int, bezeich:string, fdecimal:Decimal, fchar:string):

    prepare_cache ([Htparam])

    success_flag = False
    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, htparam
        nonlocal paramno, bezeich, fdecimal, fchar

        return {"success_flag": success_flag}


    htparam = get_cache (Htparam, {"paramnr": [(eq, paramno)]})

    if htparam:
        htparam.bezeichnung = bezeich
        htparam.fdecimal =  to_decimal(fdecimal)
        htparam.fchar = fchar


        success_flag = True
        pass

    return generate_output()