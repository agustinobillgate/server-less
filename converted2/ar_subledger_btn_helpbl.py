#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def ar_subledger_btn_helpbl(gastno:int):

    prepare_cache ([Guest])

    guest_name = ""
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_name, guest
        nonlocal gastno

        return {"guest_name": guest_name}


    guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})
    guest_name = guest.name

    return generate_output()