#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def na_start_update_flagbl(htparam_recid:int):

    prepare_cache ([Htparam])

    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam
        nonlocal htparam_recid

        return {}


    htparam = get_cache (Htparam, {"_recid": [(eq, htparam_recid)]})
    htparam.flogical = False

    return generate_output()