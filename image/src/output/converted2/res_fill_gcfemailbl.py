#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def res_fill_gcfemailbl(inp_gastnr:int, email_str:string):

    prepare_cache ([Guest])

    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest
        nonlocal inp_gastnr, email_str

        return {}


    guest = get_cache (Guest, {"gastnr": [(eq, inp_gastnr)]})
    pass
    guest.email_adr = email_str
    pass

    return generate_output()