#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 26/11/2025, with_for_update
#------------------------------------------
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


    # guest = get_cache (Guest, {"gastnr": [(eq, inp_gastnr)]})
    guest = db_session.query(Guest).filter(
            (Guest.gastnr == inp_gastnr)).with_for_update().first()
    pass
    guest.email_adr = email_str
    pass

    return generate_output()