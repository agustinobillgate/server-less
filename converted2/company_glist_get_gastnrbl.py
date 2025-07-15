#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def company_glist_get_gastnrbl(from_name:string):

    prepare_cache ([Guest])

    curr_gastnr = 0
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_gastnr, guest
        nonlocal from_name

        return {"from_name": from_name, "curr_gastnr": curr_gastnr}


    guest = get_cache (Guest, {"name": [(eq, from_name)],"gastnr": [(gt, 0)]})

    if not guest and from_name != "":
        curr_gastnr = 0
    else:
        curr_gastnr = guest.gastnr
        from_name = guest.name

    return generate_output()