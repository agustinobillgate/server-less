#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def akt_account_btn_gcfbl(curr_gastnr:int):

    prepare_cache ([Guest])

    karteityp = 0
    gastnr = 0
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal karteityp, gastnr, guest
        nonlocal curr_gastnr

        return {"karteityp": karteityp, "gastnr": gastnr}


    guest = get_cache (Guest, {"gastnr": [(eq, curr_gastnr)]})

    if guest:
        karteityp = guest.karteityp
        gastnr = guest.gastnr

    return generate_output()