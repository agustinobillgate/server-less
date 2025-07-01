#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def ba_plan_btn_guestbl(gastnr:int):

    prepare_cache ([Guest])

    guest_gastnr = 0
    avail_guest = False
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_gastnr, avail_guest, guest
        nonlocal gastnr

        return {"guest_gastnr": guest_gastnr, "avail_guest": avail_guest}


    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    if guest:
        guest_gastnr = guest.gastnr
        avail_guest = True

    return generate_output()