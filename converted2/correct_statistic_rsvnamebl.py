#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def correct_statistic_rsvnamebl(a_int:int):

    prepare_cache ([Guest])

    guestname = ""
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestname, guest
        nonlocal a_int

        return {"guestname": guestname}


    guest = get_cache (Guest, {"gastnr": [(eq, a_int)]})

    if guest:
        guestname = guest.name

    return generate_output()