#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.nt_egstat import nt_egstat
from models import Htparam

def nt_engineering():

    prepare_cache ([Htparam])

    htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 319)]})

    if htparam.paramgruppe != 99 or htparam.flogical == False:

        return generate_output()
    else:
        get_output(nt_egstat())

    return generate_output()