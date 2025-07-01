#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def mk_aktline_of_lname2bl(gastnr:int):

    prepare_cache ([Guest])

    lname = ""
    guest_gastnr = 0
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lname, guest_gastnr, guest
        nonlocal gastnr

        return {"lname": lname, "guest_gastnr": guest_gastnr}


    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
    lname = guest.name + ", " + guest.anredefirma

    return generate_output()