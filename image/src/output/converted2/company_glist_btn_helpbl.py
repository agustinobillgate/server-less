#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def company_glist_btn_helpbl(gastnr:int):

    prepare_cache ([Guest])

    from_name = ""
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_name, guest
        nonlocal gastnr

        return {"from_name": from_name}


    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
    from_name = guest.name

    return generate_output()