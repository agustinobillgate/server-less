#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def mk_aktline_btn_help2_1bl(akt_line1_gastnr:int):
    avail_guest = False
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_guest, guest
        nonlocal akt_line1_gastnr

        return {"avail_guest": avail_guest}


    guest = get_cache (Guest, {"gastnr": [(eq, akt_line1_gastnr)]})

    if not guest:
        pass
    else:
        avail_guest = True

    return generate_output()