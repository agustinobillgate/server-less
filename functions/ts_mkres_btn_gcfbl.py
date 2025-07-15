#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def ts_mkres_btn_gcfbl(gastno:int):

    prepare_cache ([Guest])

    gname = ""
    telefon = ""
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, telefon, guest
        nonlocal gastno

        return {"gname": gname, "telefon": telefon}


    guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})

    if guest:
        gname = guest.name + "," + guest.vorname1
        telefon = guest.telefon

    return generate_output()